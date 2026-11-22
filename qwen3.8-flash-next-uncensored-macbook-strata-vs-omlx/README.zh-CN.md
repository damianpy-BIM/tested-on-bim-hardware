# 在一台 MacBook（M5 Max 128 GB）上运行无审查版 Qwen3.8-Flash-Next：Strata 对比 oMLX，512K 上下文，完全用本地已有权重重建

[English](README.md)

我们手上已经有一份无审查版 Qwen3.8-Flash-Next（MLX 格式，每权重 4.8 位，101 GB）。不再下载任何新权重，直接在本机把它重建成两个 2 位模型：

- **oQ2e-mtp**，用于 oMLX（72 GB，oMLX 自带量化器，带校准，保留 MTP）
- **Q2_0 GGUF**，用于 Strata（39.8 GB，另加一个从 SSD 读取的 54.4 GB n-gram 表），由我们的转换脚本 `scripts/build_strata_q2.py` 生成

然后在同一台 Mac 上分别测试两个引擎：一次只跑一个引擎，GPU 上没有其他任务。

## 结果（MacBook Pro M5 Max，40 核 GPU，128 GB，macOS 26.6.2）

每次都用全新提示（无缓存命中），除特别说明外回复长度为 512 个 token。

| 引擎、模型、KV 缓存 | 上下文 | 预填充 (prefill) | 解码 (decode) |
|---|---|---|---|
| Strata Q2_0，KV：K 8 位 / V 4 位 | 4k | 1,868 tok/s | 63.6 tok/s |
| | 32k | 2,129 tok/s | 62.9 tok/s |
| | 128k | 1,819 tok/s | 59.3 tok/s |
| | 493k（YaRN ×2） | 1,582 tok/s | 82.3 tok/s（53 token 回答） |
| Strata Q2_0，KV 8 位（int8） | 254k（原生） | 1,655 tok/s | 62.8 tok/s（约 400 token 回答） |
| oMLX oQ2e-mtp，KV 8 位 | 4k | 2,545 tok/s | 70.8 tok/s |
| | 32k | 1,772 tok/s | 58.3 tok/s |
| | 128k | 1,941 tok/s | 46.4 tok/s |
| | 493k（YaRN ×2） | 1,695 tok/s | 9.1 tok/s（53 token 回答） |
| oMLX oQ2e-mtp，KV 4 位 | 4k | 2,057 tok/s | 67.2 tok/s |
| | 32k | 1,985 tok/s | 59.7 tok/s |
| | 128k | 2,002 tok/s | 51.8 tok/s |
| | 254k（原生） | 1,974 tok/s | 37.3 tok/s（约 400 token 回答） |
| | 493k（YaRN ×2） | 1,446 tok/s | 30.1 tok/s（约 400 token 回答） |

所有行的配置：TurboQuant 关闭；投机解码开启（Strata 每步 4 个草稿 token；oMLX 使用 Lightning MTP）。模型量化：Strata 为 Q2_0 专家层 + 其余投影 8 位；oMLX 为 oQ2e（oMLX「增强」2 位，约 2.9 bpw）。oMLX 0.8.2，Strata Terminal 0.1.63（Metal 引擎）。

结论：
- **预填充速度两者相当**，在所有长度下都在 1,450–2,550 tok/s 之间。
- **解码：Strata 随上下文增长基本不降（4k 到 254k 约 60 tok/s），oMLX 明显下降**（4 位 KV 时从 71 降到 37 tok/s）。可能的原因（尚未验证）：该模型的注意力层只选取最相关的 2,048 个历史 token（QSA indexer），而 Strata 的内核利用了这一点。
- **YaRN ×2（524,288 token）在两个引擎上都可用。** 在 493,266 token 处做“大海捞针”测试，在 10%、50%、90% 深度各放一条信息：**两个引擎都 3/3 全部找到**。不用 YaRN、在 254,445 token 处同样 3/3。

正确性测试（`scripts/quality.py`，两个引擎相同的 11 项）：数学 4/4、生成可运行并通过断言的 Python 代码、工具调用、法语和中文回答、JSON 提取、边界请求不拒答。两者都是 10/11；唯一“未通过”的是我们的题目本身有歧义（苹果题，3.5 也是合理答案）。

## 复现步骤

### 需要准备
- 128 GB 内存的 Apple Silicon Mac（64 GB 可用 Strata 的 SSD 流式加载，本文未测试）。
- 源权重：[orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored)（BF16，360 GB），或它的任意 MLX 量化版本（我们用的是一个混合 4.8 bpw 的 MLX 版本；公开的同类版本例如 [ddark-il/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/ddark-il/Qwen3.8-Flash-Next-Uncensored)）。
- 引擎：[oMLX](https://github.com/jundot/omlx) 0.8.2，以及 Strata Terminal 0.1.63 darwin-arm64（Metal 引擎，安装包 `strata-terminal-0.1.63-darwin-arm64.tar.gz`；介绍见 [modelfit.io](https://modelfit.io/blog/strata-qwen38-flash-next-mac/)）。
- 转换规则参照 llama.cpp 的 [`conversion/qwen4exp.py`](https://github.com/ggml-org/llama.cpp/blob/master/conversion/qwen4exp.py) 和 [`conversion/qwen.py`](https://github.com/ggml-org/llama.cpp/blob/master/conversion/qwen.py)。
- 仅需一个 GGUF **文件头**（约 11 MB，不是权重）：来自 [SC117/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-GGUF](https://huggingface.co/SC117/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-GGUF)，转换脚本会复制其张量布局和元数据。

### 命令
与英文版 [README.md](README.md) 的「Steps」一节完全相同：
1. `scripts/dequant.py`：MLX → bf16（逐张量）
2. `scripts/build_oq2e.py`：生成 oMLX oQ2e-mtp（同时生成第 4 步要用的校准文件 imatrix.npz）
3. 用 `curl -r` 只下载两个模板 GGUF 的文件头（各约 11 MB / 1 MB）
4. `scripts/build_strata_q2.py`：从 bf16 生成 Strata Q2_0 GGUF（按 imatrix 加权选择 2 位缩放），以及 n-gram 表文件
5. Strata 自带的 `iq_pack.py` 生成 pack，然后 `strata serve --profile configs/strata-262k.json`（或 `configs/strata-512k-yarn.json`）

oMLX 使用 512K 时，把 `configs/omlx-oq2e-config-yarn512k.json` 作为模型的 `config.json`（YaRN 因子 2，原始 262,144）。

### 踩过的坑
- Mac 上**一次只运行一个大模型任务**：oMLX 加载着模型的同时再跑转换脚本（或 Strata），我们的 Mac 因内存不足崩溃过。
- oMLX 内存上限太紧时会拒绝长提示：80 GB 的模型，128k 以上请把上限设为约 108 GB，热缓存设为 2 GB。
- Strata Metal 引擎：`--kv int8` 有一次启动失败（`kv_block_bytes has no Metal implementation yet`），之后再次启动成功；`k8v4`（K 8 位、V 4 位）每次都能启动。
- 投机解码下回复太短会夸大解码速度：请用几百个 token 的回复来测。

本仓库不包含任何权重。代码：MIT 许可。由 BIM Computing 在自有硬件上实测 — https://www.bim-computing.com

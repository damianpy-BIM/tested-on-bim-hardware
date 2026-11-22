# Offline accuracy run against OUR local oMLX server (built-in oMLX datasets + scorers, nothing uploaded).
# usage: acc.py <model_id> <out.jsonl>   greedy, thinking off, same fixed-seed samples for every model.
import sys, os, json, asyncio, httpx, time
sys.path.insert(0, "/Applications/oMLX.app/Contents/Resources")
from omlx.eval import MMLUBenchmark, GSM8KBenchmark, ARCChallengeBenchmark, HellaSwagBenchmark
PLAN = [(MMLUBenchmark, 300), (ARCChallengeBenchmark, 200), (HellaSwagBenchmark, 200), (GSM8KBenchmark, 200)]
B = "http://127.0.0.1:8000/v1"; K = os.environ.get("OMLX_API_KEY", "")
M, OUT = sys.argv[1], sys.argv[2]; CONC = 2
done = set()
if os.path.exists(OUT):
    for l in open(OUT): r = json.loads(l); done.add((r["bench"], r["i"]))
async def ask(c, msgs, mt):
    body = {"model": M, "messages": msgs, "max_tokens": mt, "temperature": 0, "chat_template_kwargs": {"enable_thinking": False}}
    for t in range(3):
        try:
            r = await c.post(B + "/chat/completions", json=body, headers={"Authorization": "Bearer " + K}, timeout=1800)
            r.raise_for_status(); return r.json()["choices"][0]["message"]["content"] or ""
        except Exception as e:
            if t == 2: raise
            await asyncio.sleep(10)
async def main():
    async with httpx.AsyncClient() as c:
        f = open(OUT, "a")
        for cls, n in PLAN:
            b = cls(); items = await b.load_dataset(n); sem = asyncio.Semaphore(CONC); t0 = time.time()
            async def one(i, it):
                if (b.name, i) in done: return
                async with sem:
                    resp = await ask(c, b.format_prompt(it), b.get_max_tokens())
                pred = b.extract_answer(resp, it); ok = bool(b.check_answer(pred, it))
                f.write(json.dumps({"bench": b.name, "i": i, "pred": pred, "ok": ok, "resp": resp[-400:]}) + "\n"); f.flush()
            await asyncio.gather(*[one(i, it) for i, it in enumerate(items)])
            rs = [json.loads(l) for l in open(OUT) if json.loads(l)["bench"] == b.name]
            print(M, b.name, f"{sum(r['ok'] for r in rs)}/{len(rs)}", f"{time.time()-t0:.0f}s", flush=True)
asyncio.run(main())

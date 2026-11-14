#!/bin/bash
# Build and test deepseek-ai/dsh-superagent-prototype in a throwaway sandbox (bubblewrap): your home directory is hidden,
# no GPU is visible, the network is used only for the clone and the package install.
# Usage: NODE_DIR=/path/to/node-v22 ./run.sh [workdir]     (Node.js >= 22.19, bwrap installed)
set -u
W=${1:-$PWD/dsh-run}; mkdir -p "$W"
NODE_DIR=${NODE_DIR:-$(dirname "$(dirname "$(command -v node)")")}
COMMIT=8c32a9dc5d72c033816c6a8110b37f40cf94fba4          # the commit we measured
cat > "$W/inner.sh" <<IN
set -u
export HOME=/w PATH=/opt/node/bin:/w/.npm-global/bin:/usr/bin:/bin CUDA_VISIBLE_DEVICES=
cd /w
t(){ local s=\$(date +%s.%N); "\$@"; local rc=\$?; echo "STEP rc=\$rc secs=\$(echo "\$(date +%s.%N) - \$s" | bc) :: \$*"; return \$rc; }
echo "node \$(node --version) cpus \$(nproc)"
[ -d repo ] || t git clone https://github.com/deepseek-ai/dsh-superagent-prototype.git repo
cd repo && git checkout -q $COMMIT
npm install -g pnpm@11.7.0 --prefix /w/.npm-global >/dev/null 2>&1
t pnpm install --no-frozen-lockfile 2>&1 | tail -5
t pnpm typecheck 2>&1 | tail -5
t pnpm test 2>&1 | tail -25
t pnpm build 2>&1 | tail -8
IN
RESOLV=(); [ -d /run/systemd/resolve ] && RESOLV=(--ro-bind /run/systemd/resolve /run/systemd/resolve)
bwrap --ro-bind /usr /usr --ro-bind /etc /etc --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin \
  "${RESOLV[@]}" --proc /proc --dev /dev --tmpfs /tmp --tmpfs /home --ro-bind "$NODE_DIR" /opt/node --bind "$W" /w \
  --unshare-all --share-net --die-with-parent bash /w/inner.sh 2>&1 | tee "$W/run.log"

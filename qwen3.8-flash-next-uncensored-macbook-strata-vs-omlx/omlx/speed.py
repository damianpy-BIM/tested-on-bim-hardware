import httpx, json, time, uuid, sys, asyncio, glob, os
B="http://127.0.0.1:8000/v1"; K=os.environ.get("OMLX_API_KEY","")
import sys as _s; M=_s.argv.pop(1)
H={"Authorization":"Bearer "+K}
TEXT=open("/Applications/oMLX.app/Contents/Resources/omlx/admin/bench_corpora/novel_en.txt").read()*2  # text bundled with oMLX (~2.4M chars, enough for 512k tokens)
def prompt(n_tok):  # ~4 chars/token, unique prefix defeats the prefix cache
    return f"[run {uuid.uuid4()}]\n" + TEXT[:n_tok*4] + "\n\nSummarise the rules above in 5 bullet points."
async def one(c, n_tok, out=256):
    t0=time.time(); ttft=None; pt=ct=0
    body={"model":M,"messages":[{"role":"user","content":prompt(n_tok)}],"max_tokens":out,"temperature":0,"stream":True,"stream_options":{"include_usage":True},"chat_template_kwargs":{"enable_thinking":False}}
    async with c.stream("POST",B+"/chat/completions",json=body,headers=H,timeout=3600) as r:
        async for l in r.aiter_lines():
            if not l.startswith("data: ") or l=="data: [DONE]": continue
            d=json.loads(l[6:])
            if d.get("choices") and d["choices"][0].get("delta",{}).get("content") and ttft is None: ttft=time.time()-t0
            if d.get("usage"): pt=d["usage"]["prompt_tokens"]; ct=d["usage"]["completion_tokens"]
    tot=time.time()-t0; ttft=ttft or tot
    return dict(prompt=pt,out=ct,ttft=round(ttft,2),prefill=round(pt/ttft,1),decode=round((ct-1)/max(tot-ttft,1e-6),1),total=round(tot,2))
# OOM guards (23/11/2026: Q3 86 GB at 262k context hard-reset the MacBook at 03:49).
# 1) budget: a row runs only if model GB + ~0.09 GB per 1k prompt tokens + 4 GB margin fits the 108 GB GPU ceiling.
#    linear fit from 3 points (Q2 72 GB ok @266k, Q3 86 GB ok @148k / reset @262k); refine with measured peaks.
# 2) live: free memory (kern.memorystatus_level) under 5 % during a request = request cancelled, row marked ABORTED.
import subprocess
CEIL_GB=108; COEF=float(os.environ.get('COEF','0.09')); SIZE_GB=int(subprocess.run(["du","-skL",os.path.expanduser("~/.omlx/models/"+M)],capture_output=True,text=True).stdout.split()[0])/1048576
def free_pct(): return int(subprocess.run(["sysctl","-n","kern.memorystatus_level"],capture_output=True,text=True).stdout)
LOW=[100]
async def watch(task):
    while not task.done():
        f=free_pct(); LOW[0]=min(LOW[0],f)
        if f<5: task.cancel(); return True
        await asyncio.sleep(1)
    return False
async def run(n_tok, conc, out=256):
    need=SIZE_GB+COEF*n_tok*conc/1000+4
    if need>CEIL_GB: print(json.dumps(dict(prompt_tok=n_tok,concurrent=conc,SKIPPED=f"needs ~{need:.0f} GB > {CEIL_GB} GB ceiling")),flush=True); return
    async with httpx.AsyncClient() as c:
        LOW[0]=F0=free_pct(); t0=time.time(); g=asyncio.ensure_future(asyncio.gather(*[one(c,n_tok,out) for _ in range(conc)])); w_=asyncio.ensure_future(watch(g))
        try: rs=await g
        except asyncio.CancelledError: print(json.dumps(dict(prompt_tok=n_tok,concurrent=conc,ABORTED="free memory < 5 %")),flush=True); return
        w=time.time()-t0
    agg_p=sum(r["prompt"] for r in rs)/max(r["ttft"] for r in rs); agg_d=sum(r["out"] for r in rs)/w
    print(json.dumps(dict(free_before=F0,free_min=LOW[0],prompt_tok=n_tok,concurrent=conc,wall=round(w,1),agg_prefill=round(agg_p,1),agg_out_tok_s=round(agg_d,1),each=rs)),flush=True)
plan=[(int(a),int(b),int(c)) for a,b,c in (x.split(":") for x in sys.argv[1:])]  # tokens:conc:out
for n,cc,o in plan: asyncio.run(run(n,cc,o))

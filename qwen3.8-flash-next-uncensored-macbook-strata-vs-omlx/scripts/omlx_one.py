import json, urllib.request, sys, random
K=""; U="http://127.0.0.1:8000/v1/chat/completions"
depth=int(sys.argv[1]); out=int(sys.argv[2]); seed=sys.argv[3] if len(sys.argv)>3 else "a"
random.seed(seed); words="server invoice harbour lantern river market engine ledger copper garden station winter".split()
txt=" ".join(random.choice(words)+str(random.randint(0,99)) for _ in range(int(depth*0.34)))
body={"model":"Qwen3.8-Flash-Next-Uncensored-oQ2e-mtp","messages":[{"role":"user","content":txt+"\n\nIgnore the list above. Write a long story about a lighthouse keeper."}],
      "max_tokens":out,"stream":False,"chat_template_kwargs":{"enable_thinking":False}}
rq=urllib.request.Request(U,json.dumps(body).encode(),{"Authorization":"Bearer "+K,"Content-Type":"application/json"})
d=json.loads(urllib.request.urlopen(rq,timeout=3600).read()); u=d["usage"]
print(json.dumps({"depth":depth,"prompt":u["prompt_tokens"],"cached":u.get("prompt_tokens_details",{}).get("cached_tokens"),"prefill":u.get("prompt_tokens_per_second"),"decode":u.get("generation_tokens_per_second"),"out":u["completion_tokens"]}))

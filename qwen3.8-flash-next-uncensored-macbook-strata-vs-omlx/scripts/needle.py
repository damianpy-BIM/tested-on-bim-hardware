import json, urllib.request, sys, random, time
U, MODEL, TOK = sys.argv[1], sys.argv[2], int(sys.argv[3]); KEY = sys.argv[4] if len(sys.argv) > 4 else ""
random.seed(42)
topics = ["harbour", "orchard", "railway", "foundry", "library", "vineyard", "observatory", "market", "glacier", "mill"]
def para(i):
    t = random.choice(topics)
    return f"Section {i}. The {t} records for this period describe routine work, weather notes, deliveries and repairs, with nothing unusual reported by the staff on duty. "
needles = {0.10: "The secret code for the blue vault is 7319-ORCA.",
           0.50: "Captain Ilse Varga keeps her spare compass inside a red tea tin.",
           0.90: "The password for the night ferry is 'lantern minus eleven'."}
n_para = int(TOK / 33)          # ~33 tokens per paragraph
parts = [para(i) for i in range(n_para)]
for frac, s in sorted(needles.items(), reverse=True): parts.insert(int(n_para * frac), s + " ")
doc = "".join(parts)
q = ("Answer from the document only, one line each, then write a 300-word summary of the document:\n1. What is the secret code for the blue vault?\n"
     "2. Where does Captain Ilse Varga keep her spare compass?\n3. What is the password for the night ferry?")
body = {"model": MODEL, "messages": [{"role": "user", "content": q + "\n\n<document>\n" + doc + "\n</document>\n\n" + q}],
        "max_tokens": 400, "temperature": 0, "stream": False, "chat_template_kwargs": {"enable_thinking": False}}
h = {"Content-Type": "application/json"}
if KEY: h["Authorization"] = "Bearer " + KEY
t0 = time.time(); d = json.loads(urllib.request.urlopen(urllib.request.Request(U, json.dumps(body).encode(), h), timeout=7200).read())
a = d["choices"][0]["message"]["content"]; u = d.get("usage", {}); t = d.get("timings", {})
hits = [("7319-ORCA" in a), ("tea tin" in a.lower()), ("lantern minus eleven" in a.lower())]
print(json.dumps({"prompt_tokens": u.get("prompt_tokens"), "secs": round(time.time() - t0), "prefill": t.get("prompt_per_second") or u.get("prompt_tokens_per_second"),
                  "decode": t.get("predicted_per_second") or u.get("generation_tokens_per_second"), "hits": hits, "answer": a.strip()[:300]}))


import requests, re, random
from config import HF_API_KEY

#change below model to this if required --> "sentence-transformers/all-mpnet-base-v2"
MODEL="sentence-transformers/all-MiniLM-L6-v2"
API=f"https://router.huggingface.co/hf-inference/models/{MODEL}"
HEAD={"Authorization":f"Bearer {HF_API_KEY}"}
TH=0.72
DEMOS=[("how to delete my account","how do i remove my account"),
       ("start the game","begin the game"),
       ("nearest hospital to me","closest clinic near me"),
       ("mobile games are getting bigger in size","game size on phones is increasing"),
       ("is it going to rain today","today is rainy"),
       ("reset my password","change my password")]

TOK=lambda s:" | ".join(s.split())
bar=lambda s:"█"*int(s*10)+"░"*(10-int(s*10))
clean=lambda t:[w for w in (re.sub(r"[^a-z0-9']+","",x.lower()) for x in t.split()) if w]
nums=lambda t:set(re.findall(r"\d+(?:\.\d+)?", t))
has_any=lambda t,arr:any(a in set(clean(t)) for a in arr)

def hf(q1,q2):
    r=requests.post(API,headers=HEAD,json={"inputs":{"source_sentence":q1,"sentences":[q2]}},timeout=30)
    if not r.ok: raise RuntimeError(r.text)
    data=r.json()
    if isinstance(data,dict): raise RuntimeError(data.get("error",str(data)))
    return float(data[0])

def smart_score(base,q1,q2,strong):
    w1={w for w in clean(q1) if len(w)>=4}; w2={w for w in clean(q2) if len(w)>=4}
    jac=len(w1&w2)/max(1,len(w1|w2))
    boost=(0.04 if len(strong)>=2 else 0)+(0.03 if jac>=0.20 else 0)+(0.05 if jac>=0.35 else 0)
    negA=["not","no","never","without","can't","cant","cannot","don't","dont","won't","wont","n't"]
    oppA=[("increase","decrease"),("bigger","smaller"),("more","less"),("add","remove"),("open","close"),("enable","disable")]
    num_pen=0.10 if (nums(q1) and nums(q2) and nums(q1)!=nums(q2)) else 0
    neg_pen=0.12 if has_any(q1,negA)!=has_any(q2,negA) else 0
    opp_pen=0.12 if any((has_any(q1,[a]) and has_any(q2,[b])) or (has_any(q1,[b]) and has_any(q2,[a])) for a,b in oppA) else 0
    return max(0.0, min(1.0, base+boost-num_pen-neg_pen-opp_pen))

def label(s): return "✅ DUPLICATE" if s>=TH else ("🤔 CLOSE MATCH" if s>=TH-0.05 else "❌ DIFFERENT")
def show_result(s):
    print(f"\n🎯 Result of Similarity: {round(s*100,1)}% [{bar(s)}]  →  {label(s)}")
    print(f"Rule: score ≥ {TH} means DUPLICATE")

def show_flow(q1,q2):
    a,b=clean(q1),clean(q2); raw=set(a+b)
    w1={w for w in a if len(w)>=4}; w2={w for w in b if len(w)>=4}
    shared=sorted(w1&w2)
    helpers=sorted({w for w in raw if 2<=len(w)<=3})
    conn={"a","an","the","to","of","in","on","is","am","are","do","did","does","my","me","it"}
    least=sorted({w for w in raw if len(w)<=2 or w in conn})
    print("\n🔁 FLOW (sentence → strongest/helper/least → similarity %)")
    print("\n1) Input sentences"); print(f"   Q1: {q1}\n   Q2: {q2}")
    print("\n2) Split into words/tokens (same as you typed)")
    print("   Q1 →",TOK(q1)); print("   Q2 →",TOK(q2))
    print("\n3) Pick the “meaning-carrying” parts (from YOUR sentences)")
    print("   Strongest:",", ".join(shared) if shared else "No obvious shared/synonym matches")
    print("   Helper:",", ".join(helpers) if helpers else "None")
    print("   Least:",", ".join(least) if least else "None")
    print("\n4) Why similarity is high/low for THIS pair")
    print("   - Direct matches:",", ".join(shared)) if shared else print("   - The model used overall meaning patterns, not exact word matches.")

def run(q1,q2,title):
    print(f"\n--- {title} ---")
    base=hf(q1,q2)
    strong=sorted({w for w in clean(q1) if len(w)>=4} & {w for w in clean(q2) if len(w)>=4})
    s=smart_score(base,q1,q2,strong)
    show_result(s); show_flow(q1,q2)

def main():
    print("Type Question 1 → Question 2. Then you’ll see 2 RANDOM demo pairs.")
    print("Type 'exit' anytime to quit.\n")
    while True:
        q1=input("Question 1: ").strip()
        if q1.lower()=="exit": break
        q2=input("Question 2: ").strip()
        if q2.lower()=="exit": break
        if not q1 or not q2: continue
        try:
            run(q1,q2,"YOUR QUESTIONS")
            for i,(d1,d2) in enumerate(random.sample(DEMOS,2),1): run(d1,d2,f"RANDOM DEMO {i}")
            print("\n(Next round → Question 1 or 'exit')\n")
        except Exception as e:
            print("\n⚠️ Oops!",e,"\n")

if __name__=="__main__":    main()
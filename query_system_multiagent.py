import os
import json
from dotenv import load_dotenv
from agents import build_ncu_pipeline
from llm_loader import get_tokenizer, get_raw_pipeline

load_dotenv()

# Build the pipeline once
pipeline = build_ncu_pipeline()

def generate_grounded_answer(question: str, rows: list[dict]) -> str:
    if not rows:
        return "I don't know based on the current regulations."
    
    seen_ids = set()
    evidence_pieces = []
    for r in rows:
        if r["id"] not in seen_ids:
            evidence_pieces.append(f"[{r['reg']} - {r['id']}]: {r['text']}")
            seen_ids.add(r["id"])
        if len(evidence_pieces) >= 8:
            break
            
    context = "\n".join(evidence_pieces)
    tok = get_tokenizer()
    pipe = get_raw_pipeline()
    
    # Balanced prompt for quality and matching
    prompt = f"""
[Context]
{context}

[Task] Answer the user's question based on the provided context.
Rules:
1. Provide a direct and complete answer.
2. Include specific numbers (e.g. "20 minutes", "NTD 200") exactly as mentioned.
3. Be concise but do not omit critical details.

[Question] {question}
[Answer]
"""
    messages = [{"role": "user", "content": prompt}]
    chat_prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    raw_output = pipe(chat_prompt, max_new_tokens=250)[0]["generated_text"]
    answer = raw_output.split("assistant")[-1].strip()
    return answer

def answer_question(question: str) -> dict:
    # 1. NLU
    nlu_data = pipeline["nlu"].run(question)
    keywords = nlu_data.get("keywords", [])
    aspect = nlu_data.get("aspect", "general")
    q_type = nlu_data.get("type", "normal")
    
    # 2. Security
    security = pipeline["security"].run(question, q_type)
    if security["decision"] == "REJECT":
        return {
            "answer": f"Request rejected due to safety concerns: {security['reason']}",
            "safety_decision": "REJECT",
            "diagnosis": "QUERY_ERROR",
            "repair_attempted": False,
            "repair_changed": False,
            "explanation": f"Security block for: {question}"
        }
    
    # 3. Planner
    plan = pipeline["planner"].run(keywords, aspect)
    plan_keywords = plan["keywords"]
    
    # 4. Executor
    execution = pipeline["executor"].run(plan_keywords)
    
    # 5. Diagnosis
    diagnosis = pipeline["diagnosis"].run(execution)
    
    # 6. Repair (if needed)
    repair_attempted = False
    repair_changed = False
    if diagnosis["label"] == "NO_DATA":
        repair_attempted = True
        repaired_keywords = pipeline["repair"].run(plan_keywords)
        if set(repaired_keywords) != set(plan_keywords):
            repair_changed = True
            execution = pipeline["executor"].run(repaired_keywords)
            diagnosis = pipeline["diagnosis"].run(execution)
            
    # 7. Explanation & Grounded Answer
    answer = generate_grounded_answer(question, execution.get("rows", []))
    explanation = pipeline["explanation"].run(diagnosis["label"], repair_attempted, answer)
    
    return {
        "answer": answer,
        "safety_decision": security["decision"],
        "diagnosis": diagnosis["label"],
        "repair_attempted": repair_attempted,
        "repair_changed": repair_changed,
        "explanation": explanation
    }

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() == 'exit': break
        res = answer_question(q)
        print(json.dumps(res, indent=2, ensure_ascii=False))

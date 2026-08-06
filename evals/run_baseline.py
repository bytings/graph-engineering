import json, time, os
from agents.llm import call, UsageLedger
from evals.score import score_item

DATASET = "evals/dataset.jsonl"
PROMPT_FILE = "evals/prompt_baseline.txt"
RUN_DIR = "runs/baseline"

os.makedirs(RUN_DIR, exist_ok=True)

with open(PROMPT_FILE) as f:
    base_prompt = f.read()

ledger = UsageLedger()
scores = []
start_time = time.time()

with open(DATASET) as f:
    for line in f:
        item = json.loads(line)
        prompt = f"{base_prompt}\n\nCode:\n{item['input']}"
        output, usage = call(prompt, max_tokens=500, effort="low")
        ledger.add(usage)

        result = score_item(item["expected"], output)
        scores.append(result["score"])

        out_path = os.path.join(RUN_DIR, f"{item['id']}.json")
        with open(out_path, "w") as outf:
            json.dump({"id": item["id"], "output": output, "score": result}, outf, indent=2)

summary = {
    "mean_score": sum(scores)/len(scores),
    "scores": scores,
    "usage": ledger.summary(),
    "wall_clock_time": time.time() - start_time,
    "model_id": "claude-3-5-sonnet",
    "effort": "low",
    "dataset_version": "v1"
}

with open(os.path.join(RUN_DIR, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("Baseline run complete. Mean score:", summary["mean_score"])

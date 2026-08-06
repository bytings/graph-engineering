import json
from agents.llm import call

def clean_output(output: str) -> str:
    text = output.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()

def deterministic_score(expected: dict, output: str) -> dict:
    output = clean_output(output)
    try:
        parsed = json.loads(output)
        found = parsed.get("defects", [])
    except Exception:
        return {"score": 0.0, "detail": {"error": "invalid JSON"}}

    expected_defects = expected.get("defects", [])
    found_set = set(d.get("rationale", "").lower() for d in found)
    expected_set = set(d.get("rationale", "").lower() for d in expected_defects)

    tp = len(found_set & expected_set)
    fp = len(found_set - expected_set)
    fn = len(expected_set - found_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (2*precision*recall)/(precision+recall) if (precision+recall) > 0 else 0

    return {"score": f1, "detail": {"precision": precision, "recall": recall, "tp": tp, "fp": fp, "fn": fn}}

def judge_score(expected: dict, output: str, input_code: str) -> dict:
    judge_prompt = f"""
You are a strict evaluator. Given a code snippet, the expected defects, and the model's output,
decide if the output correctly identifies the expected defects. Return JSON with keys:
- score (float 0–1)
- cited_text (the part of the output you based your judgment on)
- comments (short explanation)

Code:
{input_code}

Expected defects:
{json.dumps(expected, indent=2)}

Model output:
{output}

Respond ONLY with JSON.
"""
    judged_output, _ = call(judge_prompt, max_tokens=300, effort="low")
    try:
        parsed = json.loads(clean_output(judged_output))
        return {"score": parsed.get("score", 0.0), "detail": parsed}
    except Exception:
        return {"score": 0.0, "detail": {"error": "invalid judge output"}}

def score_item(expected: dict, output: str, input_code: str = "") -> dict:
    det = deterministic_score(expected, output)
    judge = judge_score(expected, output, input_code)
    combined = 0.7 * det["score"] + 0.3 * judge["score"]
    return {
        "score": combined,
        "detail": {
            "deterministic": det,
            "judge": judge,
            "combined": combined
        }
    }

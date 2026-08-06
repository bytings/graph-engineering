from agents.llm import call, UsageLedger

ledger = UsageLedger()

prompt = "In one sentence, state what an agentic workflow is."

# Effort = low
text_low, usage_low = call(prompt, max_tokens=200, effort="low")
ledger.add(usage_low)
print("\n--- response (low effort) ---")
print(text_low)
print("\n--- usage (low effort) ---")
print(usage_low.summary())

# Effort = high
text_high, usage_high = call(prompt, max_tokens=200, effort="high")
ledger.add(usage_high)
print("\n--- response (high effort) ---")
print(text_high)
print("\n--- usage (high effort) ---")
print(usage_high.summary())

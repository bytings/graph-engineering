# agents/llm.py
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic()

MODEL = "claude-sonnet-5"  # documented substitution

class UsageLedger(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0

    def add(self, usage):
        self.input_tokens += usage.input_tokens
        self.output_tokens += usage.output_tokens

    def total(self):
        return self.input_tokens + self.output_tokens

    def summary(self):
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total": self.total()
        }

def call(prompt: str, max_tokens: int = 200, effort: str = "high"):
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        output_config={"effort": effort}
    )
    usage = UsageLedger(
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens
    )
    return response.content[0].text, usage

def call_json(prompt: str, schema: dict, max_tokens: int = 200, effort: str = "high"):
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json", "schema": schema},
        output_config={"effort": effort}
    )
    return response.content[0].json

def count_tokens(prompt: str):
    return client.count_tokens(model=MODEL, messages=[{"role": "user", "content": prompt}])

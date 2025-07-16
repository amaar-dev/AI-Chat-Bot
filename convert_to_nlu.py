from collections import defaultdict
import json

with open("Intent.json", "r") as file:
    data = json.load(file)

# Try common nesting keys
if isinstance(data, dict):
    if "intents" in data:
        data = data["intents"]
    elif "data" in data:
        data = data["data"]
    elif "examples" in data:
        data = data["examples"]

intents = defaultdict(list)

for item in data:
    intent = item.get("intent")
    text_items = item.get("text")
    if isinstance(text_items, str):
        intents[intent].append(text_items)
    elif isinstance(text_items, list):
        for t in text_items:
            intents[intent].append(t.strip())

with open("nlu.yml", "w") as out:
    out.write('version: "3.1"\nnlu:\n')
    for intent, examples in intents.items():
        out.write(f"- intent: {intent}\n  examples: |\n")
        for ex in examples:
            out.write(f"    - {ex}\n")

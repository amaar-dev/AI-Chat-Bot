import json
from collections import defaultdict

# Load your JSON file
with open("Intent.json", "r") as file:
    data = json.load(file)

# Group examples by intent
intents = defaultdict(list)
for item in data:
    intents[item["intent"]].append(item["text"])

# Build Rasa NLU YAML content
with open("nlu.yml", "w") as out:
    out.write("version: \"3.1\"\n")
    out.write("nlu:\n")
    for intent, examples in intents.items():
        out.write(f"- intent: {intent}\n")
        out.write("  examples: |\n")
        for example in examples:
            out.write(f"    - {example.strip()}\n")

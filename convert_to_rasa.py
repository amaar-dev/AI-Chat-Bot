import json
import yaml

# Load JSON
with open('Intent.json', 'r') as f:
    data = json.load(f)

# --- NLU and Domain Setup ---
nlu_data = {"version": "3.1", "nlu": []}
domain_data = {
    "version": "3.1",
    "intents": [],
    "responses": {}
}
stories = {
    "version": "3.1",
    "stories": []
}

# Helper: annotate entities in a message
def annotate_entities(message, entities):
    for entity in sorted(entities, key=lambda e: e["rangeFrom"], reverse=True):
        start = entity["rangeFrom"]
        end = entity["rangeTo"]
        if start < len(message) and end <= len(message):
            value = message[start:end]
            ent_name = entity["entity"]
            annotated = f"[{value}]({ent_name})"
            message = message[:start] + annotated + message[end:]
    return message

# Loop over intents
for intent_block in data["intents"]:
    intent_name = intent_block["intent"]
    examples = []
    domain_data["intents"].append(intent_name)

    # Handle training examples
    for i, text in enumerate(intent_block["text"]):
        # Filter entities for this example
        relevant_entities = []
        for ent in intent_block.get("entities", []):
            if i >= ent["rangeFrom"] and i < ent["rangeTo"]:
                relevant_entities.append(ent)
        examples.append(f"- {annotate_entities(text, relevant_entities)}")

    nlu_data["nlu"].append({
        "intent": intent_name,
        "examples": "\n".join(examples)
    })

    # Handle bot responses
    if intent_block.get("responses"):
        domain_data["responses"][f"utter_{intent_name}"] = [
            {"text": r} for r in intent_block["responses"]
        ]

        # Simple story flow
        stories["stories"].append({
            "story": f"{intent_name} path",
            "steps": [
                {"intent": intent_name},
                {"action": f"utter_{intent_name}"}
            ]
        })

# Save files
with open("nlu.yml", "w") as f:
    yaml.dump(nlu_data, f, allow_unicode=True, sort_keys=False)

with open("domain.yml", "w") as f:
    yaml.dump(domain_data, f, allow_unicode=True, sort_keys=False)

with open("data/stories.yml", "w") as f:
    yaml.dump(stories, f, allow_unicode=True, sort_keys=False)

print("✅ nlu.yml, domain.yml, and stories.yml generated successfully.")


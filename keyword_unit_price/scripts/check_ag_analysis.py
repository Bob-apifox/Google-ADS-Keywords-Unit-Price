import json

with open("ag_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for key, val in data.items():
    if "18845390" in str(key) or "18845390" in str(val):
        print(f"Key: {key}")
        print(f"Val: {val}")

for key, val in data.items():
    if "Mintlify" in str(key) or "Mintlify" in str(val):
        print(f"Mintlify Key: {key}")
        print(f"Mintlify Val: {val}")

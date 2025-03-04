import json

#merge txt with json
refrigerator_json = "merged_data_refrigerator.json"  
dishwasher_txt = "parts_data_dishwasher.txt"        
output_file = "merged_appliances_data.json"

with open(refrigerator_json, "r", encoding="utf-8") as f:
    fridge_data = json.load(f)
with open(dishwasher_txt, "r", encoding="utf-8") as f:
    try:
        dishwasher_data = json.load(f)  
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {dishwasher_txt}: {e}")
        dishwasher_data = {}

merged_data = {
    "Refrigerator": fridge_data,
    "Dishwasher": dishwasher_data
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=4)

print(f"Both JSON files merged successfully! Saved as `{output_file}`")

import os
import json

#MERGE ALL JSONS 
json_dir = "./"  

output_file = "merged_parts_data.json"
merged_data = {}
for file in os.listdir(json_dir):
    if file.endswith("_data.json"): 
        file_path = os.path.join(json_dir, file)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                brand_data = json.load(f)
                merged_data.update(brand_data)  
                print(f"Merged {file}")
            except json.JSONDecodeError as e:
                print(f"Error loading {file}: {e}")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=4)

print(f"All JSON files merged successfully! Saved as `{output_file}`")

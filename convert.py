import json
import uuid

# Load your dataset (replace with actual file name)
input_file = "baree/data/dataset.json"
output_file = "baree/data/dataset_uuid.json"

# Read JSON data
with open(input_file, "r") as f:
    data = json.load(f)

# Dictionary to track old int PK → new UUID mapping
pk_mapping = {}

# Convert each product's integer `pk` to UUID
for item in data:
    if item["model"] == "products.product":  # Ensure we modify only Product objects
        old_pk = item["pk"]  # Integer pk
        new_uuid = str(uuid.uuid4())  # Generate new UUID
        
        pk_mapping[old_pk] = new_uuid  # Store mapping
        
        # Replace pk with new UUID
        item["pk"] = new_uuid

# Save the updated dataset
with open(output_file, "w") as f:
    json.dump(data, f, indent=4)

print(f"Dataset converted successfully! Saved as {output_file}")

import json
import os
import sys

def process_json(json_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Prepend the OUTPUT_DIR environment variable to the image_folder attribute
    output_dir = os.environ.get('OUTPUT_DIR', '')
    if 'image_folder' in data:
        data['image_folder'] = os.path.join(output_dir, data['image_folder'])
    
    # Write the modified object back to the same JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=3)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_data.py <json_file_path>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    process_json(json_file_path)
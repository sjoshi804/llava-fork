import json
import os
import sys

def process_json(json_file_path, output_dir):
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Prepend the OUTPUT_DIR environment variable to the image_folder attribute
    if 'image_folder' in data:
        data['image_folder'] = os.path.join(output_dir, data['image_folder'])
    else:
        raise ValueError("JSON file does not contain 'image_folder' attribute")
    
    # Write the modified object back to the same JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=3)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_data.py <json_file_path> <output_dir>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    output_dir = sys.argv[2]
    process_json(json_file_path, output_dir)
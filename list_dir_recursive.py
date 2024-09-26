import os
import sys

def list_dir_recursive(path, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f'{indent}{os.path.basename(root)}/')
            f.write(f'{indent}{os.path.basename(root)}/\n')
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                print(f'{sub_indent}{file}')
                f.write(f'{sub_indent}{file}\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_dir_structure.py <path>")
        sys.exit(1)
    
    path = sys.argv[1]
    output_file = 'output_test.txt'
    list_dir_recursive(path, output_file)

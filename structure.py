import os

def print_directory_structure(root_dir, output_file):
    with open(output_file, 'w') as file:
        for root, dirs, files in os.walk(root_dir):
            # Exclude __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']

            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            file.write(f'{indent}{os.path.basename(root)}/\n')

            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                # Exclude .pyc files
                if not f.endswith('.pyc'):
                    file.write(f'{sub_indent}{f}\n')


# Example usage:
root_directory = '/Users/raecephjudesayson/Desktop/Moneyme/src'  # Replace with your actual directory
output_file = 'directory_structure.txt'    # Output file

print_directory_structure(root_directory, output_file)

print(f'Directory structure has been saved to {output_file}')

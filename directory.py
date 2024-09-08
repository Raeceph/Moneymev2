import os

def extract_code_from_files(directory, output_file, exclude_dir):
    with open(output_file, 'w') as outfile:
        for root, dirs, files in os.walk(directory):
            # Exclude the specified directory
            if exclude_dir in dirs:
                dirs.remove(exclude_dir)
                
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    outfile.write(f'# {file}\n')
                    with open(filepath, 'r') as f:
                        code = f.read()
                        outfile.write(f'{code}\n')

# Example usage:
directory_to_scan = '/Users/raecephjudesayson/Desktop/Moneyme/src'
output_file = 'codes_output.txt'
directory_to_exclude = '.env'
extract_code_from_files(directory_to_scan, output_file, directory_to_exclude)

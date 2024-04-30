import os
import re

# Define the directory and file names
directory = 'model/checkpoint'
input_file = 'checkpoint2'
output_file = 'checkpoint'

# Get the absolute path of the directory
abs_directory = os.path.abspath(directory)

# Open the input file
with open(os.path.join(directory, input_file), 'r') as f:
    lines = f.readlines()

# Process each line
for i, line in enumerate(lines):
    if 'model_checkpoint_path' in line:
        # Extract the filename
        filename = re.search(r'"(.*)"', line).group(1).split('/')[-1]
        
        # Construct the new model checkpoint path
        new_model_path = os.path.join(abs_directory, filename)
        
        # Update the model checkpoint path
        lines[i] = f'model_checkpoint_path: "{new_model_path}"\n'

# Write the output file
with open(os.path.join(directory, output_file), 'w') as f:
    f.writelines(lines)

import os
import re

input_dir = "media/icon_files/light"
output_dir = "media/icon_files/dark"

for file in os.listdir(input_dir):
    if file.lower().endswith(".svg"):
        print("Converting ", file)

        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file)

        output = []

        with open(input_path, 'r') as fid:
            for line in fid:
                output_line = re.sub(r"#000000", r"#ffffff", line)

                output.append(output_line)

        with open(output_path, 'w') as fid:
            fid.write("".join(output))


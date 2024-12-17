import argparse
import base64
import os

def generate_unique_header(directory, start_tag='_FILE_'):
    found_unique = False
    current_tag = start_tag

    while not found_unique:
        dupe_found = False
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(directory, filename)

                        
                try:
                    with open(filepath, 'r', encoding='utf-8') as text_file:
                        proposed_line = f'# {current_tag}'
                        for line in text_file:
                            dupe_found = proposed_line in line
                            if dupe_found:
                                current_tag = f'_{current_tag}_'
                                break
                except UnicodeDecodeError:
                    pass

                # end for filename in files
                if dupe_found:
                    break

            # for ... os.walk(...)
            if dupe_found:
                break

        # should break outer while
        found_unique = not dupe_found

    return current_tag

def generate_single_document(directory, output_file):
    unique_header = generate_unique_header(directory)
    output_filepath = f'./{output_file}'

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(directory, filename)
                if filepath == output_filepath:
                    continue

                outfile.write(f'# {unique_header}: {filepath}\n')

                if filename.endswith('.png'):
                    with open(filepath, 'rb') as img_file:
                        outfile.write('![Embedded Image](data:image/png;base64,')

                        try:
                            full_file = img_file.read()
                            contents = base64.b64encode(full_file).decode('utf-8')
                            outfile.write(contents)
                        except:
                            pass

                        outfile.write(')\n')
                else:
                    with open(filepath, 'r') as txt_file:
                        for line in txt_file:
                            outfile.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Concatenate files and embed .png files as base64, structured as a giant Markdown file.")
    parser.add_argument(
        '-i', '--input', default='.', help="Directory (default: current directory)")
    parser.add_argument(
        '-o', '--output', default='dot.md', help="Path to the output `.md` file (default: 'dot.md')")

    args = parser.parse_args()

    generate_single_document(args.input, args.output)
    print(f"Concatenated markdown file created at {args.output}")

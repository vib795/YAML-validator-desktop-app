import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import yaml
import logging

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml;*.yml")])
    if file_path:
        with open(file_path, 'r') as file:
            txt_input.delete('1.0', tk.END)
            txt_input.insert(tk.END, file.read())

def validate_yaml():
    yaml_content = txt_input.get("1.0", tk.END)
    try:
        yaml.safe_load(yaml_content)
        messagebox.showinfo("Success", "YAML is valid!")
    except yaml.YAMLError as exc:
        corrected_yaml = attempt_correction(yaml_content)
        txt_input.delete('1.0', tk.END)
        txt_input.insert(tk.END, corrected_yaml)

        error_msg = f"Error in YAML: {str(exc)}"
        messagebox.showerror("Error Corrected", error_msg + "\n\nAttempted auto-correction applied. Please review the corrected YAML.")
        logging.error(error_msg)

def attempt_correction(yaml_str):
    # Replace tabs with spaces
    yaml_str = yaml_str.replace('\t', '    ')
    lines = yaml_str.split('\n')
    corrected_lines = []

    # Initialize a variable to track the expected indentation level
    expected_indent = None

    for i, line in enumerate(lines):
        stripped_line = line.lstrip()
        current_indent = len(line) - len(stripped_line)

        if not stripped_line:
            corrected_lines.append(line)  # Keep empty lines as is
            continue

        # Check if the line starts a new block or a list item
        if stripped_line.startswith('- ') or ':' in stripped_line:
            if expected_indent is None:
                expected_indent = current_indent
            # Adjust indentation to the expected level
            corrected_line = ' ' * expected_indent + stripped_line
            corrected_lines.append(corrected_line)
        else:
            # For lines that are part of the same block, maintain their relative indentation
            if expected_indent is not None:
                relative_indent = max(0, current_indent - expected_indent)
                corrected_line = ' ' * (expected_indent + relative_indent) + stripped_line
                corrected_lines.append(corrected_line)
            else:
                corrected_lines.append(line)

        # Reset expected indentation if this line ends a block
        if stripped_line.endswith(':') and not (i < len(lines) - 1 and lines[i + 1].lstrip().startswith('-')):
            expected_indent = None

    return '\n'.join(corrected_lines)



# Set up the window
window = tk.Tk()
window.title("YAML Validator")

# Text area for YAML input
txt_input = scrolledtext.ScrolledText(window, height=20, width=80)
txt_input.pack()

btn_validate = tk.Button(window, text="Validate & Correct YAML", command=validate_yaml)
btn_validate.pack()

# Start the GUI event loop
window.mainloop()
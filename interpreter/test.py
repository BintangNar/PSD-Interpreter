import sys
from interpreter import run  # Import the run function from your interpreter module

def interpret_file(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except IOError as e:
        print(f"Error: Unable to read '{filename}': {e}")
        return

    result, error = run(text)  # Pass only `text` if `run()` takes one argument
    if error:
        print(error.as_string())
    else:
        print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test.py <filename>")
    else:
        filename = sys.argv[1]
        interpret_file(filename)

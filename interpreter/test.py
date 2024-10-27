import argparse
import interpreter  # Import your interpreter

def interpret_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
    interpreter.run(text)  # Call the run function directly

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run a code file with the interpreter.')
    parser.add_argument('filename', type=str, help='The path to the code file to interpret (e.g., code.oyy)')

    args = parser.parse_args()  # Parse the command-line arguments
    interpret_file(args.filename)  # Pass the specified filename to interpret_file

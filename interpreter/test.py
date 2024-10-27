from interpreter import run
def run_file(filename):
    try:
        with open(filename, 'r') as f:
            code = f.read()
        result, error = run(code)
        
        if error:
            print(error.as_string())  # Display the error details if any
        else:
            print(result)  # Display the output of the interpreter
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Please provide a filename to run.")
    else:
        filename = sys.argv[1]
        run_file(filename)
#C:/Users/BINTANG/AppData/Local/Microsoft/WindowsApps/python3.11.exe c:/Users/BINTANG/strukdat/interpreter/test.py C:/Users/BINTANG/strukdat/interpreter/code.oyy

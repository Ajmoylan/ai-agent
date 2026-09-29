from functions.run_python_file import run_python_file


print("Running main.py without arguments:")
print(run_python_file("calculator", "main.py"))

print("\nRunning main.py with '3 + 5':")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("\nRunning tests.py:")
print(run_python_file("calculator", "tests.py"))

print("\nTrying ../main.py:")
print(run_python_file("calculator", "../main.py"))

print("\nTrying nonexistent.py:")
print(run_python_file("calculator", "nonexistent.py"))

print("\nTrying lorem.txt:")
print(run_python_file("calculator", "lorem.txt"))

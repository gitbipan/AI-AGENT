from functions.run_python_file import run_python_file

def main():
    working_dir="calculator"

    print(run_python_file(working_dir,"main.py",["3 + 5"]))

    

main()
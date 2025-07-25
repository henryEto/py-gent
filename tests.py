from functions.run_python import run_python_file


def test():
    result = run_python_file("calculator", "main.py")
    print("Test result 1:")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Test result 2:")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Test result 3:")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("Test result 4:")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print("Test result 5:")
    print(result)
    print("")


if __name__ == "__main__":
    test()

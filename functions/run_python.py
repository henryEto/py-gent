import os
from subprocess import run

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, constrained to the working directory. It returns the a formatted output that contains info about stdout, stderr and exit code.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of aguments to pass when executing the python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]) -> str:
    abs_pwd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_pwd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if abs_file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = run(
            args=["python3", abs_file_path] + args,
            capture_output=True,
            text=True,
        )

        out_str = (
            f"STDOUT:\n{completed_process.stdout}"
            if completed_process.stdout != ""
            else ""
        )
        err_str = (
            f"\nSTDERR:\n{completed_process.stderr}"
            if completed_process.stderr != ""
            else ""
        )
        exit_str = (
            f"\nProcess exited with code {completed_process.returncode}"
            if completed_process.returncode > 0
            else ""
        )

        output = "\n".join([out_str, err_str, exit_str]).strip()

        output = output if output != "" else "No output produced."
        return output

    except Exception as e:
        return f"Error executing Python file {file_path}: {e}"

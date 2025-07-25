import os

from google.genai import types

import config

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file in the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    abs_pwd = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_pwd):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    if not os.path.isfile(target_path):
        return f"Error: File not found or is not a regular file '{file_path}'"

    try:
        with open(file=target_path, mode="r") as f:
            file_content = f.read(config.max_chars)
            if os.path.getsize(target_path) > config.max_chars:
                file_content += f'[...File "{file_path}" truncated at {config.max_chars} characters]'
            return file_content
    except Exception as e:
        return f"Error reading {file_path}: {e}"

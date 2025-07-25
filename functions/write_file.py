import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes some content to a file in the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file.",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_pwd = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not file_path.startswith(abs_pwd):
        return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except Exception as e:
            return f"Error: Could not create '{os.path.dirname(file_path)}' directory."

    try:
        with open(file=file_path, mode="w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error writing {file_path}: {e}"

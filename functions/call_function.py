from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    """
    Handles the abstract task of calling one of our four functions.
    """
    function_name = function_call_part.name
    args = dict(function_call_part.args)
    if verbose:
      print(f"Calling function: {function_name} with args: {args}")
    else:
       print(f" - Calling function: {function_name}")
    
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    if function_name not in function_map:
          return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    func = function_map[function_name]
    args["working_directory"] = "./calculator"
    function_result = func(**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
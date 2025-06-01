# E2B service implementation
import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from src.logger import logging
# Load environment variables from .env
load_dotenv()

# Verify E2B API key is available
if not os.getenv("E2B_API_KEY"):
    raise RuntimeError("E2B_API_KEY not found in environment variables. Please add it to .env file")

def run_code_in_sandbox(file_path, code: str):
    """
    Runs the provided Python code in a sandboxed environment and returns the output.
    Raises RuntimeError if execution fails.
    """
    try:
        sbx = Sandbox(api_key=os.getenv("E2B_API_KEY"))
        # Upload the data file to sandbox
        with open(file_path, "rb") as f:
            file_in_sandbox = sbx.files.write(file_path, f)
            logging.info(f"File uploaded to sandbox: {file_in_sandbox}")
        
        # Modify the code to use the correct file path in sandbox
        # code = code.replace(file_path, file_in_sandbox)
        # Run the code
        result = sbx.run_code(code)
        logging
        return result
    except Exception as e:
        raise RuntimeError(f"Sandbox execution failed: {str(e)}")
        logging.error(f"Sandbox execution failed: {str(e)}")

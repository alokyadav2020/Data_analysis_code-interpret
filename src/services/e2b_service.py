# E2B service implementation
import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Verify E2B API key is available
if not os.getenv("E2B_API_KEY"):
    logger.error("E2B_API_KEY not found in environment variables")
    raise RuntimeError("E2B_API_KEY not found in environment variables. Please add it to .env file")

def run_code_in_sandbox(file_path, code: str):
    """
    Runs the provided Python code in a sandboxed environment and returns the output.
    Raises RuntimeError if execution fails.
    """
    try:
        logger.info("Initializing E2B sandbox")
        sbx = Sandbox(api_key=os.getenv("E2B_API_KEY"))
        
        # Upload the data file to sandbox
        logger.debug(f"Uploading file to sandbox: {file_path}")
        with open(file_path, "rb") as f:
            file_in_sandbox = sbx.files.write(file_path, f)
            logger.info(f"File uploaded to sandbox: {file_in_sandbox}")
        
        # Run the code
        logger.debug("Executing code in sandbox")
        logger.debug(f"Code to execute:\n{code}")
        result = sbx.run_code(code)
        logger.info("Code execution completed successfully")
        logger.debug(f"Execution result: {result}")
        
        return result

    except Exception as e:
        error_msg = f"Sandbox execution failed: {str(e)}"
        logger.exception(error_msg)
        raise RuntimeError(error_msg)

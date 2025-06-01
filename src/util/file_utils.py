import pandas as pd
from typing import IO
import logging

logger = logging.getLogger(__name__)

def read_file_content(file: IO, content_type: str) -> str:
    """
    Reads a CSV or Excel file from a file-like object and returns its first 10 rows as an HTML table string.
    """
    try:
        logger.info(f"Reading file content with type: {content_type}")
        
        file.seek(0)
        if content_type == "text/csv":
            logger.debug("Reading CSV file")
            df = pd.read_csv(file)
        else:
            logger.debug("Reading Excel file") 
            df = pd.read_excel(file)
            
        logger.debug(f"Data shape: {df.shape}")
        logger.debug(f"Columns: {list(df.columns)}")
        
        html_table = df.head(5).to_html(index=False, classes="data-table")
        logger.info("Successfully converted data to HTML table")
        
        return html_table
        
    except Exception as e:
        logger.exception(f"Error reading file content: {str(e)}")
        raise

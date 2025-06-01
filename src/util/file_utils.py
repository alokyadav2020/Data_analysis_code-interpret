import pandas as pd
from typing import IO

def read_file_content(file: IO, content_type: str) -> str:
    """
    Reads a CSV or Excel file from a file-like object and returns its first 10 rows as an HTML table string.
    """
    file.seek(0)
    if content_type == "text/csv":
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df.head(5).to_html(index=False, classes="data-table")

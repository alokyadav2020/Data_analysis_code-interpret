# Gemini service implementation
import os
from dotenv import load_dotenv
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.logger import logging
# Load environment variables from .env
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-05-20",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

def generate_analysis_code(file_path: str, chart_type: str) -> str:
    """
    Given a file path and chart type, use Gemini to generate Python code for data analysis and charting.
    """
    # Read the file to get a sample of the data
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    sample = df.head(100).to_dict()
    logging.info(f"Sample data for analysis: {sample}")
    columns = list(df.columns)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a data scientist. Given the following columns: {columns} and a sample of the data: {sample},"
        
        "to select the most relevant columns for data analysis and generate Python code to analyze the data and plot a {chart_type} using matplotlib or seaborn. Only output the code, do not explain anything. Provide only code in i string format do not write python or anythign else."),
        ("human", "Columns: {columns}\nSample: {sample}\nChart type: {chart_type}")
    ])
    chain = prompt | llm
    result = chain.invoke({
        "columns": columns,
        "sample": sample,
        "chart_type": chart_type
    })
    # result is likely an AIMessage object, not a dict
    if hasattr(result, 'content'):
        code = result.content.replace("```python", "").replace("```", "").strip()
        logging.info(f"Generated code:\n{code}")
    else:
        code = str(result).replace("```python", "").replace("```", "").strip()

        # print(code)
    return code

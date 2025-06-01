# Gemini service implementation
import os
from dotenv import load_dotenv
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key= os.getenv("GOOGLE_API_KEY"),
)

def generate_analysis_code(file_path: str, chart_type: str) -> str:
    """
    Given a file path and chart type, use Gemini to generate Python code for data analysis and charting.
    Supported chart types: line, bar, scatter, histogram, box, violin, strip, swarm, kde, heatmap, pairplot, countplot, pointplot, catplot, lmplot
    """
    try:
        logger.info(f"Generating analysis code for file: {file_path}, chart type: {chart_type}")
        
        # Read the file to get a sample of the data
        logger.debug(f"Reading file: {file_path}")
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        sample = df.head(100).to_dict()
        logger.debug(f"Sample data shape: {df.shape}")
        columns = list(df.columns)
        logger.debug(f"Available columns: {columns}")

        # Expanded chart type options for Seaborn
        available_charts = [
            "line", "bar", "scatter", "histogram", "box", "violin", "strip", "swarm", "kde", "heatmap", "pairplot", "countplot", "pointplot", "catplot", "lmplot"
        ]
        logger.debug(f"Available Seaborn chart types: {available_charts}")

        # Construct prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a data scientist. The user can select from the following Seaborn chart types: {', '.join(available_charts)}. Given the following columns: {{columns}} and a sample of the data: {{sample}}, select the most relevant columns for data analysis and generate Python code to analyze the data and plot a {{chart_type}} using matplotlib or seaborn. Only output the code, do not explain anything. Provide only code in a string format, do not write python or anything else."),
            ("human", "Columns: {columns}\nSample: {sample}\nChart type: {chart_type}")
        ])

        # Generate code
        # logger.debug("Sending prompt to Gemini")
        chain = prompt | llm
        result = chain.invoke({
            "columns": columns,
            "sample": sample,
            "chart_type": chart_type
        })

        # Extract code from result
        if hasattr(result, 'content'):
            code = result.content.replace("```python", "").replace("```", "").strip()
        else:
            code = str(result).replace("```python", "").replace("```", "").strip()

        logger.info("Successfully generated analysis code")
        logger.debug(f"Generated code:\n{code}")
        return code

    except Exception as e:
        logger.exception(f"Error generating analysis code: {str(e)}")
        raise

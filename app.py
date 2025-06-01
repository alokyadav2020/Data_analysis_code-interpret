from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import shutil
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from src.logger import logging
import os

app = FastAPI(
    title="File Upload API",
    description="An API to upload CSV or Excel files for processing.",
    version="0.1.0",
)

ALLOWED_CONTENT_TYPES = [
    "text/csv",  # CSV files
    "application/vnd.ms-excel",  # Older Excel .xls files
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # Modern Excel .xlsx files
]

# Mount static files
if not os.path.exists("static"):
    os.makedirs("static")
if not os.path.exists("templates"):
    os.makedirs("templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", summary="Main upload page")
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploadfile/", 
            summary="Upload a CSV or Excel file",
            description="Upload a file (CSV, XLS, XLSX). The file will be checked for its content type.")
async def create_upload_file(
    file: UploadFile = File(..., description="The CSV or Excel file to upload."),
    
    chartType: str = File(None)
):
    from fastapi.responses import JSONResponse
    import base64
    status_steps = []
    status_steps.append("1. File uploaded...")
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return JSONResponse(status_code=400, content={"detail": f"Invalid file type: {file.content_type}. Only CSV and Excel files (XLS, XLSX) are allowed.", "status_steps": status_steps})

    temp_dir = "temp_uploads"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    temp_path = os.path.join(temp_dir, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    status_steps.append("2. Processing file...")

    chart_type = chartType if chartType else "line"

    try:
        # Step 3: Generate code with Gemini
        from src.services.gemini_service import generate_analysis_code
        generated_code = generate_analysis_code(temp_path, chart_type)
        logging.info(f"Generated code:\n{generated_code}")

        status_steps.append("3. Code generated...")
        # Step 4: Run code in E2B sandbox
        from src.pipeline.pipeline import run_data_analysis_pipeline
        images_base64 = run_data_analysis_pipeline(temp_path, chart_type)
        logging.info(f"Generated {len(images_base64)} images.")
        status_steps.append("4. Code executed...")
        # Prepare HTML for all images
        chart_html = "".join([
            f"<img src='data:image/png;base64,{img}' style='max-width:100%;height:auto;margin-bottom:1em;' />"
            for img in images_base64
        ])
        status_steps.append("5. Chart/Graph generated and displayed below.")
    except Exception as e:
        status_steps.append("Error during code execution.")
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(e),
                "status_steps": status_steps
            }
        )
    finally:
        os.remove(temp_path)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded and processed.",
        "chart_html": chart_html,
        "generated_code": generated_code,
        "status_steps": status_steps
    }
from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.parsers.pdf_parser import parse_pdf
from app.agents.ddr_agent import run_ddr_agent
from app.rag.retriever import index_documents
from app.config import settings

router = APIRouter()


@router.post("/generate-ddr")
async def generate_ddr(
    inspection_report: UploadFile = File(...),
    thermal_report: UploadFile = File(...)
):

    inspection_path = os.path.join(
        settings.INPUT_INSPECTION_DIR,
        inspection_report.filename
    )

    thermal_path = os.path.join(
        settings.INPUT_THERMAL_DIR,
        thermal_report.filename
    )

    os.makedirs(settings.INPUT_INSPECTION_DIR, exist_ok=True)
    os.makedirs(settings.INPUT_THERMAL_DIR, exist_ok=True)

    with open(inspection_path, "wb") as f:
        shutil.copyfileobj(inspection_report.file, f)

    with open(thermal_path, "wb") as f:
        shutil.copyfileobj(thermal_report.file, f)

    # Parse PDFs
    inspection_data = parse_pdf(inspection_path)
    thermal_data = parse_pdf(thermal_path)

    inspection_text = inspection_data["text"]
    thermal_text = thermal_data["text"]

    inspection_images = inspection_data["images"]
    thermal_images = thermal_data["images"]

    all_images = inspection_images + thermal_images

    # Index documents into FAISS
    index_documents(inspection_text)
    index_documents(thermal_text)

    # Run AI agent
    report = run_ddr_agent(
        inspection_text,
        thermal_text,
        all_images
    )

    os.makedirs("output/reports", exist_ok=True)

    with open(settings.OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    return {
        "message": "DDR report generated successfully",
        "report_path": settings.OUTPUT_REPORT_PATH,
        "report": report
    }
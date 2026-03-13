import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:
    """
    Central configuration for the AI DDR Report Generator
    """

    # -----------------------------
    # API Keys
    # -----------------------------
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # -----------------------------
    # LLM Configuration
    # -----------------------------
    LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

    # -----------------------------
    # Input Directories
    # -----------------------------
    INPUT_INSPECTION_DIR = "data/input/inspection_reports"
    INPUT_THERMAL_DIR = "data/input/thermal_reports"

    # -----------------------------
    # Extracted Images
    # -----------------------------
    EXTRACTED_IMAGES_DIR = "data/extracted_images"

    # -----------------------------
    # Vector Database
    # -----------------------------
    VECTOR_DB_PATH = "data/vector_db/faiss_index"

    # -----------------------------
    # Output Report
    # -----------------------------
    OUTPUT_REPORT_PATH = "output/reports/generated_ddr.md"


# Create global settings object
settings = Settings()
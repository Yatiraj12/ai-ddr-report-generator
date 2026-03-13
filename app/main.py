from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI(
    title="AI DDR Report Generator",
    description="Generate Detailed Diagnostic Reports from inspection and thermal documents",
    version="1.0"
)

# Register API routes
app.include_router(router)

# Serve frontend files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")
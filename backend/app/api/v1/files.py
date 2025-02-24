from fastapi import APIRouter, UploadFile, File, Depends

from ...schemas.file import FileUploadResponse
from ...services.file import FileService

router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...), service: FileService = Depends()):
    return await service.process_file(file)

# storage_service.py

# from azure.storage.blob import BlobServiceClient  # type: ignore
# from app.config import AZURE_STORAGE_CONNECTION_STRING, AZURE_CONTAINER_NAME

# blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_arquivo(user_id: str, file_bytes: bytes, filename: str) -> str:
    # Temporariamente
    print(f"[INFO] Módulo de upload de arquivo está desativado no momento. Simulando upload.")
    return f"https://fakeurl.com/{user_id}/{filename}"

import os
from dotenv import load_dotenv
from google.cloud import storage
from google.cloud.exceptions import NotFound

load_dotenv()

# Obtenemos el json con las credenciales
json_gcp = os.getenv("JSON_GCP")

# Definimos el cliente
client = storage.Client.from_service_account_json(json_gcp)

# Definimos los tipos de archivo de entrada
URLTYPE_FILES = [
    "pdf", "docx", "txt", "rtf", "html", "epub", "csv",  # documentos
    "jpg", "jpeg", "png", "gif", "webp",                 # imágenes
    "mp4"                                                # videos
]

def save_in_bucket(file_name:str ,file: any ,bucket_name:str ="multi_ai_agent"):
    """ Guarda archivos en el storage de GCP 
    
    Parametros:
    
    - file_name: Nombre del archivo en GCP
    - file: Archivo que se subira en GCP
    - bucket_name: Nombre del bucket en GCP
    
    Return:
    
    - url: Direccion publica de la imagen subida
    """
    try: 
        bucket = client.get_bucket(bucket_name)
    except NotFound as e:
        raise RuntimeError(f"Bucket {bucket_name} no encontrado : {e}")
    
    blob = bucket.blob(file_name) # Creamos el blob
    
    # Subimos el archivo
    blob.upload_from_file(file, content_type=file.type)
    blob.make_public() # Lo hacemos publico
    
    return blob.public_url

def drop_file(file_name: str, bucket_name:str ="multi_ai_agent"):
    """ Elimina el archivo de el storage de GCP  
    
    Paraemtros:
    
    - file_name: Nombre del archivo en GCP
    - bucket_name: Nombre del bucket en GCP    
    """
    try: 
        bucket = client.get_bucket(bucket_name)
    except NotFound as e:
        raise RuntimeError(f"Bucket {bucket_name} no encontrado : {e}")
    
    blob = bucket.blob(file_name)
    
    if not blob.exists():
        return {"status": False, "message": f"Archivo no existe: {file_name}"}
    
    blob.delete() # Eliminamos el archivo
    
    return True

def save_report(file_name:str, file_content: str, 
            bucket_name:str = "multi_ai_agent") -> str:
    
    """ Guarda reportes de formato md durante 3 dias como maximo 
    
    Parametro:
    - file_name: Nombre que tendra el reporte en el bucket.
    - file_content: Contenido en string que tendra el reporte.
    - bucket_name: Nombre del bucket en el storage.
    
    Return:
    - url: Direccion publica del documento para descargar el informe
    """
    try: 
        bucket = client.get_bucket(bucket_name)
    except NotFound as e:
        raise RuntimeError(f"Bucket {bucket_name} no encontrado : {e}")
    
    # Creamos el objeto blob
    blob = bucket.blob(file_name)
    
    # Definimos el reporte como descargable
    blob.upload_from_string(file_content,content_type="application/octet-stream")
    blob.content_disposition = f'attachment; filename="{file_name}"'
    
    blob.patch() # Aplicamos los cambios
    blob.make_public() # Lo hacemos publico
    
    return blob.public_url

if __name__ == "__main__":
    content = "## Prueba"
    print(save_report(file_name="Test2.md",file_content=content))
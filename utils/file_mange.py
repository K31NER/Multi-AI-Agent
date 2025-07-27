import os
from dotenv import load_dotenv
from google.cloud import storage
from google.cloud.exceptions import NotFound

load_dotenv()

# Obtenemos el json con las credenciales
json_gcp = os.getenv("JSON_GCP")

# Definimos el cliente
client = storage.Client.from_service_account_json(json_gcp)

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

if __name__ == "__main__":
    pass
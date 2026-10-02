import boto3

REGION = 'us-east-2'
BUCKET_NAME = 'jjr-1110-de'
DB_NAME = 'taller_glue_db'

s3 = boto3.resource('s3', region_name=REGION)
glue = boto3.client('glue', region_name=REGION)

print("Iniciando limpieza final del Punto 6...")

# 1. Vaciar y eliminar el bucket S3
try:
    print(f"Vaciando y eliminando bucket {BUCKET_NAME}...")
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.objects.all().delete()
    bucket.delete()
    print(f"[+] Bucket {BUCKET_NAME} eliminado con éxito.")
except Exception as e:
    print(f"[-] Error con S3: {e}")

# 2. Eliminar la base de datos de Glue (esto también borra las tablas asociadas)
try:
    print(f"Eliminando base de datos de Glue {DB_NAME}...")
    glue.delete_database(Name=DB_NAME)
    print(f"[+] Base de datos {DB_NAME} y sus tablas eliminadas.")
except Exception as e:
    print(f"[-] Error con Glue: {e}")

print("\nLimpieza total completada")
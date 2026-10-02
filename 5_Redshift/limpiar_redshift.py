import boto3

REGION = 'us-east-2'
# Nombre exacto sacado de tu captura
BUCKET_NAME = 'taller-redshift-datos-1790943808' 
SECRET_NAME = 'taller-redshift-credenciales'

s3 = boto3.resource('s3', region_name=REGION)
sm = boto3.client('secretsmanager', region_name=REGION)

print("Iniciando limpieza de recursos del Punto 5...")

# 1. Vaciar y eliminar el Bucket S3
try:
    print(f"Vaciando y eliminando bucket {BUCKET_NAME}...")
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.objects.all().delete()  # S3 requiere vaciar el bucket antes de borrarlo
    bucket.delete()
    print(f"[+] Bucket {BUCKET_NAME} eliminado con éxito.")
except Exception as e: 
    print(f"[-] Error con S3: {e}")

# 2. Eliminar el Secreto de forma permanente
try:
    print(f"Eliminando secreto {SECRET_NAME}...")
    sm.delete_secret(SecretId=SECRET_NAME, ForceDeleteWithoutRecovery=True)
    print(f"[+] Secreto {SECRET_NAME} programado para eliminación permanente.")
except Exception as e: 
    print(f"[-] Error con Secrets Manager: {e}")

print("¡Limpieza completada!")
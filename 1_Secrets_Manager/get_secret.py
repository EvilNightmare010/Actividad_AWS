import boto3
import json
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "taller_db_credentials"
    region_name = "us-east-2"

    # Crear la sesión de Boto3
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Recuperar el secreto
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error al recuperar el secreto: {e}")
        raise e

    # Extraer y parsear el string JSON
    secret = response['SecretString']
    return json.loads(secret)

if __name__ == "__main__":
    credenciales = get_secret()
    print("¡Secreto recuperado con éxito!")
    print(f"Usuario: {credenciales.get('username')}")
    print(f"Contraseña: {credenciales.get('password')}")
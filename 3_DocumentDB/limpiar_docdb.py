import boto3

def limpiar_entorno_docdb():
    region = 'us-east-2'
    ec2 = boto3.client('ec2', region_name=region)
    secrets = boto3.client('secretsmanager', region_name=region)

    ec2_id = 'i-09170fc1f1b9ab6c2'
    secret_name = 'docdb_credentials_1790801469'
    key_name = 'taller_docdb_key_1790801469'

    print("1. Eliminando Secreto de Secrets Manager...")
    try:
        secrets.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)
        print(f"[+] Secreto {secret_name} eliminado.")
    except Exception as e: print(e)

    print("2. Terminando Instancia EC2 Bastion...")
    try:
        ec2.terminate_instances(InstanceIds=[ec2_id])
        print(f"[+] Instancia {ec2_id} en proceso de terminación.")
    except Exception as e: print(e)

    print("3. Eliminando Key Pair...")
    try:
        ec2.delete_key_pair(KeyName=key_name)
        print(f"[+] Key Pair {key_name} eliminado de AWS.")
    except Exception as e: print(e)

    print("\n¡Limpieza iniciada! Nota: Los Security Groups quedan vivos porque dependen de que la EC2 y DocumentDB se borren por completo (toma unos minutos), pero no generan NINGÚN cobro.")

if __name__ == "__main__":
    limpiar_entorno_docdb()
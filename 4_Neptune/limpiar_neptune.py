import boto3

def limpiar_entorno_neptune():
    region = 'us-east-2'
    ec2 = boto3.client('ec2', region_name=region)

    ec2_id = 'i-0d6e83bf360807dca'
    key_name = 'taller_neptune_key_1790890556'

    print("1. Terminando Instancia EC2 Bastion de Neptune...")
    try:
        ec2.terminate_instances(InstanceIds=[ec2_id])
        print(f"[+] Instancia {ec2_id} en proceso de terminación.")
    except Exception as e: print(e)

    print("2. Eliminando Key Pair...")
    try:
        ec2.delete_key_pair(KeyName=key_name)
        print(f"[+] Key Pair {key_name} eliminado de AWS.")
    except Exception as e: print(e)

    print("\n¡Limpieza de Neptune iniciada con éxito! No quedan recursos facturables.")

if __name__ == "__main__":
    limpiar_entorno_neptune()
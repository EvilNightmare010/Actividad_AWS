import boto3

def eliminar_infraestructura():
    region = 'us-east-2'
    s3 = boto3.client('s3', region_name=region)
    ec2 = boto3.client('ec2', region_name=region)
    rds = boto3.client('rds', region_name=region)

    bucket_name = "bucket-taller-datos-boto3-1790773971"
    sg_id = "sg-050dab4afdcb0077d"
    ec2_id = "i-00c8ff296d9b9fda2"
    rds_id = "taller-rds-boto3-1790773971"

    print("1. Eliminando Bucket S3...")
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} eliminado.")
    except Exception as e:
        print(f"Error S3: {e}")

    print("2. Terminando Instancia EC2...")
    try:
        ec2.terminate_instances(InstanceIds=[ec2_id])
        print(f"Instancia {ec2_id} en proceso de terminación.")
    except Exception as e:
        print(f"Error EC2: {e}")

    print("3. Eliminando Base de Datos RDS...")
    try:
        rds.delete_db_instance(
            DBInstanceIdentifier=rds_id, 
            SkipFinalSnapshot=True
        )
        print(f"Instancia RDS {rds_id} en proceso de eliminación.")
    except Exception as e:
        print(f"Error RDS: {e}")

    print("\nNota: El Security Group no se puede eliminar con código en este momento porque depende de que EC2 y RDS terminen de borrarse por completo (toma unos minutos).")

if __name__ == "__main__":
    eliminar_infraestructura()
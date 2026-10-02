import boto3
import time

def desplegar_infraestructura():
    region = 'us-east-2'
    s3 = boto3.client('s3', region_name=region)
    ec2 = boto3.client('ec2', region_name=region)
    rds = boto3.client('rds', region_name=region)

    timestamp = int(time.time())

    # 1. Crear Bucket S3
    bucket_name = f"bucket-taller-datos-boto3-{timestamp}"
    s3.create_bucket(
        Bucket=bucket_name, 
        CreateBucketConfiguration={'LocationConstraint': region}
    )
    print(f"[+] Bucket S3 creado: {bucket_name}")

    # 2. Crear Security Group (Red)
    vpcs = ec2.describe_vpcs()
    vpc_id = vpcs['Vpcs'][0]['VpcId']
    
    sg_name = f"taller_sg_boto3_{timestamp}"
    sg = ec2.create_security_group(
        GroupName=sg_name, 
        Description='SG Taller Boto3', 
        VpcId=vpc_id
    )
    sg_id = sg['GroupId']
    print(f"[+] Security Group creado: {sg_id}")

    # 3. Crear Instancia EC2
    instances = ec2.run_instances(
        ImageId='ami-09b90e09742640522', # Amazon Linux 2023 en us-east-2
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        SecurityGroupIds=[sg_id]
    )
    ec2_id = instances['Instances'][0]['InstanceId']
    print(f"[+] Instancia EC2 en creacion: {ec2_id}")

    # 4. Crear Base de Datos RDS con Secrets Manager
    rds_name = f"taller-rds-boto3-{timestamp}"
    rds.create_db_instance(
        DBInstanceIdentifier=rds_name,
        AllocatedStorage=20,
        DBInstanceClass='db.t3.micro',
        Engine='mysql',
        MasterUsername='adminuser',
        ManageMasterUserPassword=True, # Integración con Secrets Manager
        VpcSecurityGroupIds=[sg_id],
        PubliclyAccessible=False
    )
    print(f"[+] Instancia RDS en creacion (con Secrets Manager): {rds_name}")
    print("\n¡Despliegue con Boto3 iniciado exitosamente!")

if __name__ == "__main__":
    desplegar_infraestructura()
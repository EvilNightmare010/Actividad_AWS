import boto3
import os
import json
import time

def preparar_entorno_docdb():
    region = 'us-east-2'
    ec2 = boto3.client('ec2', region_name=region)
    secrets = boto3.client('secretsmanager', region_name=region)
    
    ts = int(time.time())

    print("Iniciando creación de infraestructura para DocumentDB...\n")

    # 1. Crear KeyPair para conectarnos por SSH
    key_name = f'taller_docdb_key_{ts}'
    key_pair = ec2.create_key_pair(KeyName=key_name)
    
    key_file = f"{key_name}.pem"
    with open(key_file, "w") as file:
        file.write(key_pair['KeyMaterial'])
    
    # Dar permisos restrictivos al archivo .pem (Obligatorio para SSH en Linux/WSL)
    os.chmod(key_file, 0o400) 
    print(f"[+] Llave SSH creada y guardada como: {key_file}")

    # 2. Crear Secreto para DocumentDB
    secret_name = f"docdb_credentials_{ts}"
    password = "AdminPassword2026!"
    secrets.create_secret(
        Name=secret_name,
        SecretString=json.dumps({"username": "docdbadmin", "password": password})
    )
    print(f"[+] Secreto '{secret_name}' creado en Secrets Manager.")

    # 3. Obtener VPC por defecto
    vpcs = ec2.describe_vpcs()
    vpc_id = vpcs['Vpcs'][0]['VpcId']

    # 4. Crear Security Groups
    sg_ec2 = ec2.create_security_group(GroupName=f"SG_EC2_Bastion_{ts}", Description="SG EC2 Bastion", VpcId=vpc_id)
    sg_ec2_id = sg_ec2['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=sg_ec2_id, 
        IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]
    )
    print(f"[+] Security Group EC2 creado: {sg_ec2_id} (Permite SSH)")

    sg_docdb = ec2.create_security_group(GroupName=f"SG_DocDB_{ts}", Description="SG DocumentDB", VpcId=vpc_id)
    sg_docdb_id = sg_docdb['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=sg_docdb_id, 
        IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 27017, 'ToPort': 27017, 'UserIdGroupPairs': [{'GroupId': sg_ec2_id}]}]
    )
    print(f"[+] Security Group DocDB creado: {sg_docdb_id} (Solo permite trafico desde el EC2)")

    # 5. Lanzar EC2 Bastion
    instances = ec2.run_instances(
        ImageId='ami-09b90e09742640522', # Amazon Linux 2023 en us-east-2
        InstanceType='t2.micro',
        KeyName=key_name,
        SecurityGroupIds=[sg_ec2_id],
        MinCount=1, MaxCount=1,
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'BastionDocDB'}]}]
    )
    ec2_id = instances['Instances'][0]['InstanceId']
    print(f"[+] Instancia EC2 (Túnel SSH) lanzada: {ec2_id}")
    
    print("\n¡Fase 1 completada exitosamente!")

if __name__ == "__main__":
    preparar_entorno_docdb()
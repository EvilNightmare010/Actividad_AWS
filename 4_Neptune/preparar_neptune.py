import boto3
import os
import time

def preparar_entorno_neptune():
    region = 'us-east-2'
    ec2 = boto3.client('ec2', region_name=region)
    ts = int(time.time())

    print("Iniciando creación de infraestructura para Neptune...\n")

    # 1. Crear KeyPair para SSH
    key_name = f'taller_neptune_key_{ts}'
    key_pair = ec2.create_key_pair(KeyName=key_name)
    key_file = f"{key_name}.pem"
    with open(key_file, "w") as file: file.write(key_pair['KeyMaterial'])
    os.chmod(key_file, 0o400) # Permisos de Linux
    print(f"[+] Llave SSH creada: {key_file}")

    # 2. Obtener VPC por defecto
    vpcs = ec2.describe_vpcs()
    vpc_id = vpcs['Vpcs'][0]['VpcId']

    # 3. Crear Security Groups (Puerto 8182 para Neptune)
    sg_ec2 = ec2.create_security_group(GroupName=f"SG_EC2_Neptune_{ts}", Description="SG EC2 Bastion", VpcId=vpc_id)
    sg_ec2_id = sg_ec2['GroupId']
    ec2.authorize_security_group_ingress(GroupId=sg_ec2_id, IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
    print(f"[+] SG EC2 Bastion creado: {sg_ec2_id}")

    sg_neptune = ec2.create_security_group(GroupName=f"SG_Neptune_{ts}", Description="SG Neptune Cluster", VpcId=vpc_id)
    sg_neptune_id = sg_neptune['GroupId']
    ec2.authorize_security_group_ingress(GroupId=sg_neptune_id, IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 8182, 'ToPort': 8182, 'UserIdGroupPairs': [{'GroupId': sg_ec2_id}]}])
    print(f"[+] SG Neptune creado: {sg_neptune_id} (Solo tráfico desde EC2)")

    # 4. Lanzar EC2 Bastion
    instances = ec2.run_instances(
        ImageId='ami-09b90e09742640522', InstanceType='t2.micro', KeyName=key_name,
        SecurityGroupIds=[sg_ec2_id], MinCount=1, MaxCount=1,
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'BastionNeptune'}]}]
    )
    ec2_id = instances['Instances'][0]['InstanceId']
    print(f"[+] Instancia EC2 (Túnel SSH) lanzada: {ec2_id}")

if __name__ == "__main__":
    preparar_entorno_neptune()
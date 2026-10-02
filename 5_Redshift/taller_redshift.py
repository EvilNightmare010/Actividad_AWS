import boto3
import time
import csv

# ================= CONFIGURACIÓN =================
REGION = 'us-east-2'
WORKGROUP = 'default-workgroup'  # Grupo de trabajo por defecto en Serverless
DB_NAME = 'dev'                  # Base de datos que creó el profe
SECRET_NAME = 'taller-redshift-credenciales'
ROLE_ARN = 'arn:aws:iam::802655955683:role/service-role/AmazonRedshift-CommandsAccessRole-20261002T065107'
BUCKET_NAME = f'taller-redshift-datos-{int(time.time())}'

# Clientes de AWS
sm = boto3.client('secretsmanager', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)
data_api = boto3.client('redshift-data', region_name=REGION)

def preparar_y_subir_datos():
    print(f"1. Creando Bucket S3: {BUCKET_NAME} y archivos locales...")
    s3.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': REGION})
    
    with open('usuarios.csv', 'w', newline='') as f:
        csv.writer(f).writerows([['id', 'nombre', 'ciudad'], [1, 'Ana', 'Medellin'], [2, 'Juan', 'Bogota'], [3, 'Carlos', 'Medellin'], [4, 'Maria', 'Cali']])
    
    with open('compras.csv', 'w', newline='') as f:
        csv.writer(f).writerows([['id_compra', 'id_usuario', 'monto'], [101, 1, 150.50], [102, 1, 45.00], [103, 2, 80.00], [104, 3, 200.00], [105, 4, 30.00]])

    print("2. Subiendo archivos a S3...")
    s3.upload_file('usuarios.csv', BUCKET_NAME, 'usuarios.csv')
    s3.upload_file('compras.csv', BUCKET_NAME, 'compras.csv')

def ejecutar_sql(sql, secret_arn, esperar_resultado=False):
    res = data_api.execute_statement(
        WorkgroupName=WORKGROUP,
        Database=DB_NAME,
        SecretArn=secret_arn,
        Sql=sql
    )
    query_id = res['Id']
    
    while True:
        status = data_api.describe_statement(Id=query_id)['Status']
        if status in ['FINISHED', 'FAILED', 'ABORTED']:
            break
        time.sleep(2)
        
    if status == 'FAILED':
        error = data_api.describe_statement(Id=query_id)['Error']
        print(f"[-] Error SQL: {error}")
        return None
        
    if esperar_resultado and status == 'FINISHED':
        return data_api.get_statement_result(Id=query_id)['Records']
    return True

def procesar_datos():
    print("3. Recuperando ARN del secreto...")
    secret_arn = sm.describe_secret(SecretId=SECRET_NAME)['ARN']

    print("4. Creando tablas en Redshift Serverless...")
    ejecutar_sql("CREATE TABLE IF NOT EXISTS usuarios (id INT, nombre VARCHAR(50), ciudad VARCHAR(50));", secret_arn)
    ejecutar_sql("CREATE TABLE IF NOT EXISTS compras (id_compra INT, id_usuario INT, monto DECIMAL(8,2));", secret_arn)

    print("5. Cargando datos desde S3 (COPY)...")
    ejecutar_sql(f"COPY usuarios FROM 's3://{BUCKET_NAME}/usuarios.csv' IAM_ROLE '{ROLE_ARN}' CSV IGNOREHEADER 1;", secret_arn)
    ejecutar_sql(f"COPY compras FROM 's3://{BUCKET_NAME}/compras.csv' IAM_ROLE '{ROLE_ARN}' CSV IGNOREHEADER 1;", secret_arn)

    print("6. Ejecutando consulta analítica (Join + Filtro + Agregación)...")
    query = """
    SELECT u.ciudad, SUM(c.monto) as total_compras
    FROM usuarios u
    JOIN compras c ON u.id = c.id_usuario
    WHERE c.monto > 50
    GROUP BY u.ciudad;
    """
    resultados = ejecutar_sql(query, secret_arn, esperar_resultado=True)
    
    if resultados:
        print("\n=== RESULTADOS DE LA CONSULTA ===")
        for fila in resultados:
            ciudad = fila[0]['stringValue']
            total = fila[1]['stringValue']
            print(f"Ciudad: {ciudad} | Total Ingresos (>50): ${total}")
        print("=================================\n")

if __name__ == "__main__":
    preparar_y_subir_datos()
    procesar_datos()
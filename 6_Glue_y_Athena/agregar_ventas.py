import boto3
import csv

REGION = 'us-east-2'
BUCKET_NAME = 'jjr-1110-de'
FILE_NAME = 'ventas_nuevas.csv'

s3 = boto3.client('s3', region_name=REGION)

def agregar_datos():
    print("1. Creando nuevos registros de ventas...")
    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id_venta', 'producto', 'categoria', 'precio', 'ciudad'])
        # Agregamos ventas muy grandes a Medellín para notar el cambio rápido
        writer.writerow([26, 'TV_Gigante', 'Electronica', 5000.00, 'Medellin'])
        writer.writerow([27, 'Sofa_Lujo', 'Hogar', 3000.00, 'Medellin'])

    print(f"2. Subiendo nuevo archivo a s3://{BUCKET_NAME}/datos/{FILE_NAME} ...")
    s3.upload_file(FILE_NAME, BUCKET_NAME, f'datos/{FILE_NAME}')
    print("[+] ¡Nuevos datos agregados al Data Lake!")

if __name__ == "__main__":
    agregar_datos()
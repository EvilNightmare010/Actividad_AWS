import boto3
import csv

REGION = 'us-east-2'
BUCKET_NAME = 'jjr-1110-de'
FILE_NAME = 'ventas_tienda.csv'

s3 = boto3.client('s3', region_name=REGION)

def generar_y_subir_datos():
    print("1. Generando archivo de datos (25 registros)...")
    
    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id_venta', 'producto', 'categoria', 'precio', 'ciudad'])
        
        for i in range(1, 26):
            categoria = 'Electronica' if i % 2 == 0 else 'Hogar'
            ciudad = 'Medellin' if i % 3 == 0 else 'Bogota'
            precio = round(10.50 * i, 2)
            writer.writerow([i, f'Producto_{i}', categoria, precio, ciudad])

    print(f"2. Subiendo archivo a s3://{BUCKET_NAME}/datos/{FILE_NAME} ...")
    s3.upload_file(FILE_NAME, BUCKET_NAME, f'datos/{FILE_NAME}')
    print("[+] Archivo subido con éxito.")

if __name__ == "__main__":
    generar_y_subir_datos()
import boto3
import json
from pymongo import MongoClient

def ejecutar_consultas():
    # 1. Recuperar credenciales de Secrets Manager
    print("Recuperando credenciales...")
    client_secrets = boto3.client('secretsmanager', region_name='us-east-2')
    response = client_secrets.get_secret_value(SecretId='docdb_credentials_1790801469')
    creds = json.loads(response['SecretString'])
    
    # 2. Conectar a DocumentDB a través del túnel local
    print("Conectando a DocumentDB...")
    client = MongoClient(
        host='localhost',
        port=27017,
        username=creds['username'],
        password=creds['password'],
        tls=True,
        tlsCAFile='global-bundle.pem',
        tlsAllowInvalidHostnames=True,
        retryWrites=False,
        directConnection=True
    )
    
    db = client['taller_db']
    coleccion = db['productos']
    coleccion.drop() # Limpiar por si se ejecuta varias veces
    
    # 3. Insertar 10 documentos
    print("Insertando 10 documentos...")
    datos = [
        {"nombre": "Laptop", "categoria": "Electronica", "precio": 1200, "stock": 15},
        {"nombre": "Mouse", "categoria": "Electronica", "precio": 25, "stock": 50},
        {"nombre": "Teclado", "categoria": "Electronica", "precio": 45, "stock": 30},
        {"nombre": "Monitor", "categoria": "Electronica", "precio": 200, "stock": 10},
        {"nombre": "Escritorio", "categoria": "Muebles", "precio": 150, "stock": 5},
        {"nombre": "Silla", "categoria": "Muebles", "precio": 80, "stock": 20},
        {"nombre": "Audifonos", "categoria": "Electronica", "precio": 60, "stock": 40},
        {"nombre": "Lampara", "categoria": "Hogar", "precio": 30, "stock": 25},
        {"nombre": "Cuaderno", "categoria": "Papeleria", "precio": 5, "stock": 100},
        {"nombre": "Boligrafo", "categoria": "Papeleria", "precio": 2, "stock": 200}
    ]
    coleccion.insert_many(datos)
    
    # 4. Búsqueda con filtro
    print("\n--- FILTRO: Productos de Electrónica ---")
    filtro = coleccion.find({"categoria": "Electronica"}, {"_id": 0, "nombre": 1, "precio": 1})
    for doc in filtro: print(doc)
        
    # 5. Ordenación
    print("\n--- ORDENACIÓN: Los 3 productos más caros ---")
    ordenados = coleccion.find({}, {"_id": 0, "nombre": 1, "precio": 1}).sort("precio", -1).limit(3)
    for doc in ordenados: print(doc)
        
    # 6. Agregación
    print("\n--- AGREGACIÓN: Precio promedio por categoría ---")
    pipeline = [{"$group": {"_id": "$categoria", "precio_promedio": {"$avg": "$precio"}}}]
    agregacion = coleccion.aggregate(pipeline)
    for doc in agregacion: print(doc)

if __name__ == "__main__":
    ejecutar_consultas()
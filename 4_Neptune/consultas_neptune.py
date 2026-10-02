from gremlin_python.driver import client
import ssl

def ejecutar_grafos():
    # 1. Configurar SSL para saltar la validación de localhost debido al túnel
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    print("Conectando a Amazon Neptune a través del túnel...")
    # CORRECCIÓN AQUÍ: Se pasa ssl=ssl_context directamente
    c = client.Client('wss://localhost:8182/gremlin', 'g', ssl=ssl_context)

    # Limpiar el grafo (por si ejecutas el script más de una vez)
    c.submit("g.V().drop()").all().result()

    # 2. Insertar 10 Vértices (Nodos)
    print("Insertando 10 vértices (Personas)...")
    nombres = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
    for nombre in nombres:
        c.submit(f"g.addV('Person').property('userid', '{nombre}').property('name', '{nombre}')").all().result()

    # 3. Insertar 15 Relaciones (Aristas)
    print("Insertando 15 relaciones (Conoce a)...")
    relaciones = [
        ("Alice", "Bob"), ("Alice", "Charlie"), ("Bob", "David"),
        ("Charlie", "David"), ("David", "Eve"), ("Eve", "Frank"),
        ("Frank", "Grace"), ("Grace", "Heidi"), ("Heidi", "Ivan"),
        ("Ivan", "Judy"), ("Judy", "Alice"), ("Bob", "Eve"),
        ("Charlie", "Frank"), ("David", "Grace"), ("Eve", "Heidi")
    ]
    for origen, destino in relaciones:
        query = f"g.V().has('userid', '{origen}').addE('knows').to(g.V().has('userid', '{destino}'))"
        c.submit(query).all().result()

    print("\n--- CONSULTAS DE RECORRIDO DE GRAFOS ---")
    
    # Consulta 1: Recorrido directo (1 salto)
    q1 = c.submit("g.V().has('userid', 'Alice').out('knows').values('name')").all().result()
    print(f"1. ¿A quién conoce Alice? -> {q1}")

    # Consulta 2: Recorrido inverso (Quién apunta hacia el nodo)
    q2 = c.submit("g.V().has('userid', 'David').in('knows').values('name')").all().result()
    print(f"2. ¿Qué personas conocen a David? -> {q2}")

    # Consulta 3: Recorrido de 2 saltos (Amigos de amigos)
    q3 = c.submit("g.V().has('userid', 'Alice').out('knows').out('knows').values('name')").all().result()
    print(f"3. Amigos de los amigos de Alice -> {q3}")

if __name__ == "__main__":
    ejecutar_grafos()
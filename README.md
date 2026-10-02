# Taller 3 - Ingeniería de Datos

Este repositorio contiene la solución completa a la Actividad de AWS enfocada en el despliegue, gestión y análisis de bases de datos y servicios de infraestructura en la nube. Todas las prácticas fueron realizadas bajo estrictos criterios de optimización de costos y seguridad, garantizando la eliminación de recursos tras su validación.

Integrantes:
- Juan José Ramírez Pulgarín
- Juan Nicolás Cortés Rincón

---

## 1. AWS Secrets Manager

**Instrucciones de Ejecución (Carpeta `1_Secrets_Manager`)**
1. Configurar el secreto en la consola de AWS.
2. Ejecutar `python get_secret.py` para recuperar el secreto usando Boto3 de forma segura.

---

## 2. Despliegue con Terraform, SDK y AWS CLI

**Instrucciones de Ejecución (Carpeta `2_Infraestructura`)**
1. **Terraform:** Navegar a la carpeta `terraform_deploy`, ejecutar `terraform init`, `terraform apply` y posteriormente `terraform destroy`.
2. **Boto3:** Ejecutar `python deploy_boto3.py` para crear los recursos y `python delete_boto3.py` para eliminarlos.
3. **AWS CLI:** Seguir los comandos listados secuencialmente en el archivo `aws_cli.txt`.

---

## 3. Amazon DocumentDB

**Instrucciones de Ejecución (Carpeta `3_DocumentDB`)**
1. Levantar el túnel SSH con la instancia EC2.
2. Ejecutar `python preparar_docdb.py`.
3. Ejecutar `python consultas_docdb.py` para realizar filtros, ordenación y agregaciones.
4. Ejecutar `python limpiar_docdb.py` para destruir los recursos.

---

## 4. Amazon Neptune

**Instrucciones de Ejecución (Carpeta `4_Neptune`)**
1. Ejecutar `python preparar_neptune.py` para instanciar vértices y relaciones.
2. Ejecutar `python consultas_neptune.py` para recorrer el grafo.
3. Ejecutar `python limpiar_neptune.py`.

---

## 5. Amazon Redshift

**Instrucciones de Ejecución (Carpeta `5_Redshift`)**
1. Ejecutar `python taller_redshift.py`. Este script usa Boto3 para generar los CSV, subirlos a S3, autenticarse vía API de Datos usando Secrets Manager, ejecutar comandos `COPY` y realizar la analítica.
2. Ejecutar `python limpiar_redshift.py` para vaciar S3 y forzar la eliminación del secreto.

---

## 6. AWS Glue Data Catalog y Amazon Athena

**Instrucciones de Ejecución (Carpeta `6_Glue_y_Athena`)**
1. Ejecutar `python taller_glue.py` para subir los datos brutos a S3.
2. Ejecutar la sentencia `CREATE EXTERNAL TABLE` directamente en la consola de Athena.
3. Ejecutar `python agregar_ventas.py` para simular entrada de nuevos datos al Data Lake.
4. Ejecutar nuevamente la consulta en Athena para evidenciar la actualización automática.
5. Ejecutar `python limpiar_glue.py` para destruir el bucket de datos y la base de datos de Glue.
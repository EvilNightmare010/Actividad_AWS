terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

# 1. Bucket S3
resource "aws_s3_bucket" "taller_bucket" {
  bucket_prefix = "bucket-taller-datos-"
  force_destroy = true # Permite borrar el bucket aunque tenga archivos
}

# 2. Grupo de Seguridad para EC2 y RDS (Red)
resource "aws_security_group" "taller_sg" {
  name        = "taller_security_group"
  description = "Permitir trafico local"

  # Regla de entrada: SSH para EC2
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Regla de entrada: MySQL para RDS (solo desde el mismo Security Group)
  ingress {
    from_port = 3306
    to_port   = 3306
    protocol  = "tcp"
    self      = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. Instancia EC2
resource "aws_instance" "taller_ec2" {
  ami           = "ami-09b90e09742640522" # Amazon Linux 2023 en us-east-2
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.taller_sg.id]

  tags = {
    Name = "TallerEC2"
  }
}

# 4. Instancia RDS (Integrada con Secrets Manager)
resource "aws_db_instance" "taller_rds" {
  identifier           = "taller-rds-mysql"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  db_name              = "tallerdb"
  username             = "adminuser"
  
  # Esta linea hace que AWS use Secrets Manager para la contraseña automáticamente
  manage_master_user_password = true 
  
  vpc_security_group_ids = [aws_security_group.taller_sg.id]
  skip_final_snapshot  = true # Necesario para poder eliminar la BD sin dejar backups cobrables
  publicly_accessible  = false
}
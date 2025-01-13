import psycopg2
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configurações do S3
bucket_name = 'nome-do-bucket'
s3_path = 'dados-vendas/'
region_name = 'us-east-1'  # Substitua pela sua região
s3_uri = f's3://{bucket_name}/{s3_path}'

# Configurações do Redshift
redshift_host = 'seu-cluster-name.redshift.amazonaws.com'
redshift_dbname = 'seu-db-name'
redshift_user = 'seu-usuario'
redshift_password = 'sua-senha'
redshift_port = 5439
iam_role = 'arn:aws:iam::your-account-id:role/RedshiftS3Role'  # Substitua pelo seu ARN de role IAM

# Função para se conectar ao Redshift
def connect_redshift():
    try:
        conn = psycopg2.connect(
            dbname=redshift_dbname,
            user=redshift_user,
            password=redshift_password,
            host=redshift_host,
            port=redshift_port
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao Redshift: {e}")
        return None

# Função para executar o comando COPY
def copy_data_to_redshift(conn):
    # Criação de um cursor
    cur = conn.cursor()
    
    # Comando COPY para carregar dados do S3 para o Redshift
    copy_sql = f"""
    COPY sales
    FROM '{s3_uri}'
    CREDENTIALS 'aws_iam_role={iam_role}'
    CSV
    IGNOREHEADER 1
    DELIMITER ','
    REGION '{region_name}';
    """
    
    try:
        print("Iniciando o processo de cópia de dados do S3 para o Redshift...")
        cur.execute(copy_sql)
        conn.commit()
        print("Dados copiados com sucesso!")
    except Exception as e:
        print(f"Erro ao executar o COPY: {e}")
    finally:
        cur.close()

# Função principal
def main():
    # Conectar ao Redshift
    conn = connect_redshift()
    
    if conn:
        # Copiar os dados para o Redshift
        copy_data_to_redshift(conn)
        # Fechar a conexão
        conn.close()

if __name__ == '__main__':
    main()

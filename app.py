import requests
from datetime import datetime
import boto3
import json

def lambda_handler(event, context):

    now = datetime.now()
    fecha=str(now.strftime("%Y-%m-%d"))
    url = 'https://casas.mitula.com.co/searchRE/op-1/tipo-Casa/q-Chapinero--Cundinamarca'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    def name_archivo(fecha):
        return 'landing_casas_'+fecha+'.html'
    
    name_file=name_archivo(fecha)   
     
    def get_fincaraiz_results(url, headers):
        response = requests.get(url, headers=headers)
        a=response.text.encode(encoding="utf-8")
        return a

    client = boto3.client('s3')
    def save_to_s3(data, filename, bucket_name, client):
        #con el método put_object se carga el archivo al bucket indicado con el nombre guardado en la variable name_txt
        client.put_object(Body=data,Bucket=bucket_name,Key=filename)
    
    # Guarda la salida en un bucket de S3
    save_to_s3(get_fincaraiz_results(url, headers), name_file, 'landing-casas-brayan', client)
    
    return {
            'statusCode': 200,
            'body': json.dumps('html generado!')
    }
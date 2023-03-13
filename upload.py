import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import boto3

def lambda_handler(event, context):
    
    now = datetime.now()
    date_hoy=str(now.strftime("%Y-%m-%d"))

    def name_archivo(fecha):
        return 'landing_casas_'+fecha+'.html'
    
    name_file=name_archivo(date_hoy) 
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('landing-casas-brayan')
    obj = bucket.Object(name_file)
    html_content = obj.get()['Body'].read()

    def set_mi_tula(html_content):

        soup = BeautifulSoup(html_content, 'html.parser')
        script = soup.find('script', {'type': 'application/ld+json'})
        script_text = script.text
        json_data = json.loads(script_text)
        price = soup.find_all('div', class_='price')
        precio=[precio.text for precio in price]
        
        return json_data, precio

    json_data, precio= set_mi_tula(html_content)


    data_x=[]
    
    def clean_information(json, b):
        for valores in json:
            for value in b:
                data_x.append([
                    date_hoy,
                    valores.get('address',{}).get('addressLocality', 'NA'),
                    value, 
                    valores.get('numberOfBedrooms', 0),
                    valores.get('numberOfBathroomsTotal', 0), 
                    valores.get('floorSize', {}).get('value', 0)])
                break
        return data_x

    informacion_to_csv=clean_information(json_data['about'], precio)
    
    
    client = boto3.client('s3')
    
    def save_to_s3(data, filename, bucket_name, client):
        #con el método put_object se carga el archivo al bucket indicado con el nombre guardado en la variable name_txt
        client.put_object(Body=data,Bucket=bucket_name,Key=filename)
        

    # Convierte los datos a una cadena de texto en formato CSV
    columnas = ['fecha descarga', 'Ciudad', 'precio', 'Número habitaciones', 'Número baños', 'área (mt2)']
    csv_data = ",".join(columnas) + "\n"
    csv_data += "\n".join([",".join(map(str, row)) for row in informacion_to_csv])   
    
    
    def name_final(fecha):
        return 'casas_final_'+fecha+'.csv'
         
    name_upload=name_final(date_hoy)
    # Guarda la salida en un bucket de S3
    save_to_s3(csv_data.encode(), name_upload, 'casas-final-brayan', client)  

    return {
            'statusCode': 200,
            'body': json.dumps('csv generado')
        }

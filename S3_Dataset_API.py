import re
import sys
import json
import boto3
import requests
import io
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from boto3.session import Session

# Global vars
API_URL = 'https://datausa.io/api/data?drilldowns=Nation&measures=Population'
BASE_URL = 'https://download.bls.gov'
EXT_URL = '/pub/time.series/pr/'
FOLDER_URL = 'pr/'
BUCKET = 'rearcdataquest'

def get_s3_session():
    AWS_KEY_ID = ''
    AWS_SECRET = ''
    session = Session(aws_access_key_id=AWS_KEY_ID, aws_secret_access_key=AWS_SECRET)
    s3 = session.resource('s3')
    return s3

def get_s3_data():
    s3 = get_s3_session()
    result = s3.meta.client.list_objects(Bucket=BUCKET, Prefix=FOLDER_URL)
    d_s3 = {el['Key'].split(FOLDER_URL)[1]: el["LastModified"].replace(tzinfo=None) 
        for el in result['Contents'] 
        if el['Key'].split(FOLDER_URL)[1] != ''}
    return d_s3

def update_s3(d_web, d_s3):
    s3 = get_s3_session()
    # Update new and existing old files
    for el in d_web:
        if (el not in d_s3) or (d_web[el] > d_s3[el]):
            content = requests.get(BASE_URL+EXT_URL+el).text
            response = s3.meta.client.put_object(Bucket=bucket, Body=bytes(content, encoding='utf-8'), Key=FOLDER_URL+el)
    # Delete files no more present in web
    for el in d_s3:
        if el not in d_web:
            response = s3.meta.client.delete_object(Bucket=bucket, Key=FOLDER_URL+el)

def get_web_data():
    res = requests.get(BASE_URL+EXT_URL)  
    # parse data result to get infos
    soup = BeautifulSoup(res.text, 'html.parser')
    text_content = soup.find('pre').getText()
    files = [node.get('href').split('/')[-1] for node in soup.find_all('a') if node.get('href').startswith(EXT_URL)]
    dates = re.findall(r'\d{1,2}.\d{1,2}.\d{4}', text_content)
    times = re.findall(r'\d{1,2}[:]\d{1,2}', text_content)
    # add info to dict structure
    temp = {k:[int(x) for x in v1.split('/')+v2.split(':')] for k, v1, v2 in zip(files, dates, times)}
    d_web = {el: datetime(temp[el][2], temp[el][0], temp[el][1], temp[el][3], temp[el][4], 59) for el in temp}
    return d_web

def get_api_data():
    s3 = get_s3_session()
    res = requests.get(API_URL)
    data = res.json()['data']
    response = s3.meta.client.put_object( 
            Bucket=BUCKET,
            Body=json.dumps(data),
            Key='population_data.json'
        )
    
def orchestrator():
    d_web = get_web_data()
    d_s3 = get_s3_data()
    update_s3(d_web, d_s3)
    get_api_data() 
    #print(d_web)
    #print(d_s3)


if __name__ == "__main__":
    orchestrator()

import pandas as pd
import json
import boto3
import io
from boto3.session import Session

# Gloal vars
BUCKET = 'rearcdataquest'

def get_s3_session():
    AWS_KEY_ID = ''
    AWS_SECRET = ''
    session = Session(aws_access_key_id=AWS_KEY_ID, aws_secret_access_key=AWS_SECRET)
    s3 = session.resource('s3')
    return s3

def read_s3_file(file_name):
    s3 = get_s3_session()
    obj = s3.Object(BUCKET, file_name)
    data = obj.get()['Body'].read()
    return data

def get_analytics():
    # Load csv file Part1
    data = read_s3_file('pr/pr.data.0.Current')
    df1 = pd.read_csv(io.BytesIO(data), sep="\t")
    df1.columns = ['series_id', 'year', 'period', 'value', 'footnote_codes']
    df1 = df1.astype({"series_id": str, "period": str})
    df1['series_id'] = df1['series_id'].str.strip()
    df1['period'] = df1['period'].str.strip()
    
    # Load json file Part2
    data = read_s3_file('population_data.json')
    df2 = pd.read_json(data)
    
    '''
    generate the mean and the standard deviation of the US population across the years [2013, 2018] inclusive.
    '''
    q = df2[(df2["ID Year"] >= 2013) & (df2["ID Year"] <= 2018)]
    mean = q['Population'].mean()
    std = q['Population'].std()
    print(f'mean = {mean}, std = {std}')
    
    '''
    Using the dataframe from the time-series (Part 1), For every series_id, find the best year: 
    the year with the max/largest sum of "value" for all quarters in that year. 
    Generate a report with each series id, the best year for that series, and the summed value for that year. 
    '''
    q = df1.groupby(['series_id','year']).sum()
    q = q.iloc[q.reset_index().groupby(['series_id'])['value'].idxmax()]
    print(q)
    
    '''
    Using both dataframes from Part 1 and Part 2, 
    generate a report that will provide the value for series_id = PRS30006032 and period = Q01 and 
    the population for that given year (if available in the population dataset)
    '''
    q = df1[(df1["series_id"] == 'PRS30006032') & (df1["period"] == 'Q01')]
    j = q.merge(df2, left_on=['year'], right_on=['ID Year'])[['series_id','year','period','value','Population']]
    print(j)

def orchestrator(event, context):
    print('RUN DATA ANALYTICS')
    get_analytics()
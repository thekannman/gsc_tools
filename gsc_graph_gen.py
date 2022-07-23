import os
import pygsheets
import pandas as pd
from googleapiclient.discovery import build
from datetime import date
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Point this to your own oauth credentials file.
oauth_file ='credentials.json'
# Needs to match your domain name in GSC. 
# For domain properties, this will be something like
# 'sc-domain:yourdomain.com'
# Otherwise, it will be:
# 'https://yourdomain.com'  
site = 'YOURDOMAIN.COM'

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/webmasters.readonly'
    ]

today = date.today().strftime('%Y-%m-%d')

credentials = None
if os.path.exists('token.json'):
    credentials = Credentials.from_authorized_user_file(
        'token.json',
        scopes=SCOPES)
if not credentials or not credentials.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        oauth_file,
        scopes=SCOPES)
    flow.run_local_server()
    credentials = flow.credentials
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

service = build('searchconsole', 'v1', credentials=credentials)
    
gc = pygsheets.authorize(custom_credentials=credentials)

dfs = []
startRow = 0
while True:
    api_request = {
        'startDate': "2022-01-01",
        'endDate': today,
        'dimensions': ['page','date'],
        'rowLimit':25000,
        'startRow':startRow,
        'dimensionFilterGroups': {
        "groupType": "and",
            "filters": [{
            "dimension": "page",
            "operator": "notContains",
            "expression": "#"
            }]
        }
    }
    response = service.searchanalytics()\
        .query(siteUrl=site, body=api_request).execute()
    if not 'rows' in response:
        break
    dfs.append(pd.DataFrame(response['rows']))
    startRow = startRow + 25000
gsc_page_date_df = pd.concat(dfs)
gsc_page_date_df['page'] = gsc_page_date_df['keys'].apply(lambda x: x[0])
gsc_page_date_df['date'] = gsc_page_date_df['keys'].apply(lambda x: x[1])
gsc_page_date_df = gsc_page_date_df[['page','date','clicks','impressions','ctr','position']]

sh = gc.create('GSC graphs - pages')
sh.add_worksheet('clicks', rows=1001)
sh.add_worksheet('impressions', rows=1001)
sh.add_worksheet('position', rows=1001)
sh.add_worksheet('compare', rows=4)
sh.del_worksheet(sh.worksheet_by_title('Sheet1'))

ws = sh.worksheet_by_title('clicks')
ws.adjust_row_height(1,ws.rows,pixel_size=100)
ws.adjust_column_width(1,ws.cols,pixel_size=300)
ws.cell((1,1)).set_value("Clicks (2022-01-01 – Current)")
model_cell = ws.cell((1,1)).set_text_format("bold", True)
ws.range('1:1',returnas='range').apply_format(model_cell)
data = [f'=if(not(isblank(B{i})),sparkline(E{i}:{i}),)' for i in range(2,1002)]
ws.set_dataframe(pd.DataFrame(data),(2,1), copy_head=False)

ws = sh.worksheet_by_title('impressions')
ws.adjust_row_height(1,ws.rows,pixel_size=100)
ws.adjust_column_width(1,ws.cols,pixel_size=300)
ws.cell((1,1)).set_value("Impressions (2022-01-01 – Current)")
model_cell = ws.cell((1,1)).set_text_format("bold", True)
ws.range('1:1',returnas='range').apply_format(model_cell)
data = [f'=if(not(isblank(B{i})),sparkline(E{i}:{i}),)' for i in range(2,1002)]
ws.set_dataframe(pd.DataFrame(data),(2,1), copy_head=False)

ws = sh.worksheet_by_title('position')
ws.adjust_row_height(1,ws.rows,pixel_size=100)
ws.adjust_column_width(1,ws.cols,pixel_size=300)
ws.cell((1,1)).set_value("Position (2022-01-01 – Current)")
model_cell = ws.cell((1,1)).set_text_format("bold", True)
ws.range('1:1',returnas='range').apply_format(model_cell)
data = [f'=if(not(isblank(B{i})),sparkline(E{i}:{i},{{"ymax",0;"ymin",max(E{i}:{i})}}),)' for i in range(2,1002)]
ws.set_dataframe(pd.DataFrame(data),(2,1), copy_head=False)

ws = sh.worksheet_by_title('compare')
ws.adjust_row_height(1,ws.rows,pixel_size=100)
ws.adjust_column_width(1,ws.cols,pixel_size=300)
ws.cell((1,1)).set_value('=transpose({clicks!B1:B})')
ws.cell((2,1)).set_value('=transpose({clicks!A1:A})')
ws.cell((3,1)).set_value('=transpose({impressions!A1:A})')
ws.cell((4,1)).set_value('=transpose({position!A1:A})')

merged_gsc_df = pd.merge(
    gsc_page_date_df.groupby('page').sum()[['clicks','impressions']],
    gsc_page_date_df.pivot('page','date','clicks').fillna('0').reset_index(), 
    on='page'
).sort_values('clicks',ascending=False)

sh.worksheet_by_title('clicks').set_dataframe(merged_gsc_df.head(1000),(1,2))

merged_gsc_df = pd.merge(
    gsc_page_date_df.groupby('page').sum()[['clicks','impressions']],
    gsc_page_date_df.pivot('page','date','impressions').fillna('0').reset_index(), 
    on='page'
).sort_values('clicks',ascending=False)

sh.worksheet_by_title('impressions').set_dataframe(merged_gsc_df.head(1000),(1,2))

merged_gsc_df = pd.merge(
    gsc_page_date_df.groupby('page').sum()[['clicks','impressions']],
    gsc_page_date_df.pivot('page','date','position').fillna('0').reset_index(), 
    on='page'
).sort_values('clicks',ascending=False)

sh.worksheet_by_title('position').set_dataframe(merged_gsc_df.head(1000),(1,2))
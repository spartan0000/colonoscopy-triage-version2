#script to send data to the api endpoint

import os
import json
import requests
from dotenv import load_dotenv
import asyncio
from pathlib import Path

load_dotenv()

BASE = Path(__file__).parent.parent
DATA_PATH = BASE / 'data' / 'sample_reports'



report_file = DATA_PATH / 'sample_patient_report_1.txt'

with open(report_file, 'r', encoding = 'utf-8') as f:
    report = f.read()



api_url = 'http://127.0.0.1:8000/triage'


async def send_request(report_text: str, api_url: str):
    '''
    Sends a free text reort to the API endpoint and returns a recommendation based on the report and database contents
    '''

    data = {'user_query': report_text}
    headers = {
        'x-api-key': os.getenv('MY_API_KEY')
    }

    response = requests.post(api_url, json = data, headers = headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'API request failed with status code {response.status_code}: {response.text}')
       
    

async def main():

    output = await send_request(report, api_url)
    print(output)

if __name__ == '__main__':
    asyncio.run(main())


#script to send data to the api endpoint

import os
import json
import requests
from dotenv import load_dotenv
import asyncio
from pathlib import Path

from client_scripts.human_key import HUMAN_LABELS

load_dotenv()

BASE = Path(__file__).parent.parent
DATA_PATH = BASE / 'data' / 'sample_reports'

n_files = len(os.listdir(DATA_PATH))


api_url = 'http://localhost:8000/triage'
base_url = os.getenv('AZURE_APP_ENDPOINT')
azure_url = f'{base_url}/triage'


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
       
    
def accuracy(human, model):
    year_correct = 0
    rule_correct = 0
    total = 0

    year_incorrect = []
    rule_incorrect = []
    need_human = []

    for item in human:
        cid = item['case']
        rec = model[cid]
        if item['follow_up'] == rec['follow_up']:
            year_correct += 1
        else:
            year_incorrect.append({'case': cid, 'human': item['follow_up'], 'model': rec['follow_up']})
        if item['rule'] == rec['rule']:
            rule_correct += 1
        else:
            rule_incorrect.append({'case': cid, 'human': item['rule'], 'model': rec['rule']})
        
        if rec['follow_up'] == 0:
            need_human.append({'case': cid, 'model': rec['rule']})
        total += 1
    year_accuracy = year_correct/total
    rule_accuracy = rule_correct/total

    return year_accuracy, rule_accuracy, year_incorrect, rule_incorrect, need_human


async def main():
    #iterate through the sample reports, pull the recommendation, add it to the model_outputs dictionary 
    model_outputs = {}
    for i in range(n_files):
        report_path = DATA_PATH / f'sample_patient_report_{i}.txt'
        with open(report_path, 'r', encoding = 'utf-8') as f:
            report = f.read()

        output = await send_request(report, azure_url)
        recommendation = output['recommendation']

        model_outputs[f'{i:03}'] = recommendation
        print(f'{i+1} report(s) processed')

    year, rule, y_incorrect, r_incorrect, need_human = accuracy(HUMAN_LABELS, model_outputs)

    print(f'Year_accuracy: {year} | Rule_accuracy: {rule}')
    print(f'Incorrect year cases: \n {y_incorrect}\n')
    print(f'Incorrect rule cases: \n {r_incorrect}\n')
    print(f'These were identified as needing human review:\n {need_human}')

    print(model_outputs)

if __name__ == '__main__':
    asyncio.run(main())


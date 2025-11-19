import openai
from openai import OpenAI, AzureOpenAI
import os
from typing import List
import json
from dotenv import load_dotenv
import yaml
from pathlib import Path

import asyncio
import requests

import random

import logging
from datetime import datetime

from clients import chat_client, embedding_client

load_dotenv()

BASE_PATH = Path(__file__).parent.parent
PROMPT_PATH = BASE_PATH / 'app' / 'prompts'
DATA_PATH = BASE_PATH / 'data' / 'sample_reports'


async def format_query_json(user_query: str) -> dict: 
    PROMPT_FILE = PROMPT_PATH/'json_summary_prompt.yaml'
    with open(PROMPT_FILE, 'r', encoding = 'utf-8') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise Exception(f'Error loading YAML prompt file: {e}')
        system_prompt = f'{config['prompt']['content']}'
        if 'rules' in config:
            rules_text = '\nRules:\n' + '\n'.join(f'- {rule}' for rule in config['rules'])
            system_prompt = f'{system_prompt}\n{rules_text}'
        
        

    user_prompt = f'Please format this medical text into structured JSON output - {user_query}'

    response1 = await chat_client.responses.create(
        model = 'gpt-5-mini',
        text = {'format': {'type': 'json_object'}},
        input = [
            {
                'role':'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': user_prompt,
            }
        ],
        

    )

    try:
        raw_output = response1.output_text
        result_json = json.loads(raw_output)
        return result_json
    except json.JSONDecodeError:
        return {'error': 'Failed to parse JSON', 'raw_output': response1.output_text}


def triage(data: dict):
    follow_up = None
    patient_age = data['patient_age']
    indication = data.get('indication', '')
    total_polyps = data['colonoscopy'][0]['number_of_polyps']
    cecum = data['colonoscopy'][0]['cecum_reached']
    bbps = data['colonoscopy'][0]['bostonBowelPrepScore']
    hist = data['colonoscopy'][0]['histology']
    n_adenoma = hist['adenomas']
    size_adenoma = hist['adenoma_size']
    hgd_adenoma = hist['high_grade_dysplasia_in_adenoma']
    tva = hist['tubulovillous_or_villous_adenoma']
    n_ssl = hist['sessile_serrated_polyps']
    size_ssl = hist['sessile_serrated_polyp_size']
    dysplastic_ssl = hist['dysplasia_in_the_sessile_serrated_polyp']
    hp_large = hist['hyperplastic_polyp_greater_or_equal_to_10mm_in_size']

    #need human review
    #for now, have follow up value of 0 represent needing human review
    if cecum == 'no':
        outcome = {'follow_up': 0, 'reason': 'Cecum not reached'}
    elif bbps < 6:
        outcome = {'follow_up': 0, 'reason':'Inadequate prep'}
    elif indication == 'sps':
        outcome = {'follow_up': 0, 'reason': 'Serrated polyposis syndrome'}
    #this seems like something a human should look at
    elif n_adenoma >= 10:
        outcome = {'follow_up': 1, 'reason': 'Greater than 10 adenomatous polyps'}

 
    #3 years
    elif size_ssl >=10:
        outcome = {'follow_up': 3, 'reason': 'SSL >= 10mm'}
    elif dysplastic_ssl == 'yes':
        outcome = {'follow_up': 3, 'reason': 'SSL with dysplasia'}
    elif size_adenoma >= 10:
        outcome = {'follow_up': 3, 'reason': 'Adenoma >= 10mm'}
    elif tva == 'yes':
        outcome = {'follow_up': 3, 'reason': 'Tubulovillous or villous adenoma'}
    elif hgd_adenoma == 'yes':
        outcome = {'follow_up': 3, 'reason': 'Adenoma with HGD'}
    elif n_adenoma == 0 and n_ssl >= 5 and size_ssl < 10:
        outcome = {'follow_up': 3, 'reason': '5 or more SSL all less than 10mm, no other polyps, no high risk features'}
    elif n_ssl == 0 and 5 <= n_adenoma <= 9 and size_adenoma < 10 and hgd_adenoma == 'no':
        outcome = {'follow_up': 3, 'reason': '5-9 adenomas with no high risk features and no SSL'}
    elif n_ssl > 0 and n_adenoma > 0 and 5 <= total_polyps <= 9:
        outcome = {'follow_up': 3, 'reason': '5-9 combined adenomas and SSL'}
    elif hp_large == 'yes':
        outcome = {'follow_up': 3, 'reason': 'Hyperplastic polyp >= 10mm'}
    


    #5 years
    elif n_ssl == 0 and 3 <= n_adenoma <= 4 and size_adenoma < 10 and hgd_adenoma == 'no':
        outcome = {'follow_up': 5, 'reason': '3-4 adenomas, no SSL, no high risk features'}
    
    elif 1 <= n_ssl <= 4 and size_ssl < 10 and n_adenoma == 0:
        outcome = {'follow_up': 5, 'reason': '1-4 SSL < 10mm no dysplasia no other polyps'}
    
    elif n_ssl > 0 and total_polyps <= 4 and size_ssl < 10 and size_adenoma < 10:
        outcome = {'follow_up': 5, 'reason': 'Adenoma and SSL present, less than 5 total polyps, no high risk features'}
    

    #10 years

    elif n_ssl == 0 and n_adenoma < 3 and size_adenoma < 10 and hgd_adenoma == 'no':
        outcome = {'follow_up': 10, 'reason': '1-2 adenomas less than 10mm no hgd'}
    
    #if no criteria met, refer for human review
    else:
        outcome = {'follow_up': 0, 'reason': 'No criteria met, needs human review'}

    #see if the patient will age out
    follow_up = outcome['follow_up']
    if follow_up is not None and follow_up + patient_age > 75:
        outcome = {'follow_up': 0, 'reason': 'Patient aged out'}
        return outcome
    else:
        return outcome




async def main():
    with open(DATA_PATH / 'sample_patient_report_1.txt', 'r', encoding = 'utf-8') as f:
        report = f.read()
    output = await format_query_json(report)
    recommendation = triage(output)
    print(f'Given this data\n {output}\n\n The recommendation is: {recommendation}')
    

if __name__ == '__main__':
    asyncio.run(main())

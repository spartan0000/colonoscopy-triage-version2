#streamlit UI  

import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
from pathlib import Path
import requests

import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

#print(sys.path)


load_dotenv()

local_url = 'http://127.0.0.1:8000/triage'
base_url = os.getenv('AZURE_APP_ENDPOINT')
azure_url = f'{base_url}/triage'

API_URL = 'http://api:8000/triage' #when running in docker container



async def send_request(report_text: str, api_url: str):
    '''
    Sends a free text report to the API endpoint and returns a recommendation based on the report and database contents
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

st.title("Colonoscopy Surveillance Triage Tool")
st.write("This tool provides surveillance interval recommendations based on the colonoscopy and histology report data you provide.")
st.write("Please enter the colonoscopy report and the associated histology report into the text box below.")
if 'report_input' not in st.session_state:
    st.session_state.report_input = ''

user_input = st.text_area("Enter colonoscopy and histology reports as single text input here:",
                           key = 'report_input',
                           value = st.session_state.report_input,
                           height = 400)
                           
def clear_text():
    st.session_state.report_input = ''

if st.button("Get Recommendation"):
    if user_input.strip() == '':
        st.error('Please enter a valid colonoscopy and histology report.')
    else:
        with st.spinner('Processing your request...'):
            try:
                output = asyncio.run(send_request(user_input, API_URL))
                recommendation = output['recommendation']

            except Exception as e:
                st.error(f'An error occurred: {e}')
    if recommendation['rule'] == 'rule_20':
        st.write("Based on the data provided, the patient has aged out of surveillance colonoscopy recommendations.")
    elif recommendation['rule'] == 'rule_23':
        st.write("Based on the data provided, the patient is discharged from surveillance colonoscopy due to a normal colonoscopy and family history category 1 or 2")
    else:
        st.write(f"Based on the data provided, the recommended follow-up interval is: {recommendation['follow_up']} years and the reason is: {recommendation['reason']}")    
    st.write(f"Full JSON Summary Output: {output['user_input']}")

st.button('Clear Text', on_click = clear_text)
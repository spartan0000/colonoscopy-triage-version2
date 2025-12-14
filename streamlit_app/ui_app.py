#streamlit UI  

import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
from pathlib import Path

import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

print(sys.path)


from app.functions import send_request

load_dotenv()

local_url = 'http://127.0.0.1:8000/triage'
base_url = os.getenv('AZURE_APP_ENDPOINT')
azure_url = f'{base_url}/triage'

st.title("Colonoscopy Surveillance Triage Tool")
st.write("This tool provides surveillance interval recommendations based on the colonoscopy and histology report data you provide.")
st.write("Please enter the colonoscopy report and the associated histology report into the text box below.")

user_input = st.text_input("Enter colonoscopy and histology reports as single text input here:")

if st.button("Get Recommendation"):
    if user_input.strip() == '':
        st.error('Please enter a valid colonoscopy and histology report.')
    else:
        with st.spinner('Processing your request...'):
            try:
                output = asyncio.run(send_request(user_input, local_url))
                recommendation = output['recommendation']
            except Exception as e:
                st.error(f'An error occurred: {e}')
        st.write(f'Based on the data provided, the recommended follow-up interval is: {recommendation['follow_up']} years and the reason is: {recommendation['reason']}')    
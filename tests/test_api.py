import pytest

from unittest.mock import AsyncMock, patch

from app import functions
from app.models.colonoscopy import ColonoscopySummary

def test_extract_structured_data_and_age_out(client, test_case1):
    fake = {'user_query': 'test text'}

    with patch("app.functions.format_query_json", new_callable=AsyncMock) as mock_return:
        mock_return.return_value = test_case1.model_dump()
        response = client.post("/triage", json = fake)
    assert mock_return.called
    assert response.status_code == 200

    data = response.json()

    assert data['recommendation'] is not None
    #age out rule number is 20 somewhat arbitrarily assigned
    assert data['recommendation']['follow_up'] == 20
    

def test_no_age_out(client, test_case1):
    fake = {'user_query': 'test text'}
    test_case = test_case1.model_dump()
    test_case['patient_age'] = 50
    with patch("app.functions.format_query_json", new_callable=AsyncMock) as mock_return:
        mock_return.return_value = test_case
        response = client.post("/triage", json = fake)
    assert response.status_code == 200
    data = response.json()

    assert data['recommendation']['follow_up'] == 10

def test_high_grade_adenoma(client, test_case1):
    fake = {'user_query': 'test text'}
    test_case = test_case1.model_dump()

    test_case['colonoscopy'][0]['polyps'][0]['dysplasia'] = 'high_grade'
    test_case['patient_age'] = 50

    with patch("app.functions.format_query_json", new_callable = AsyncMock) as mock_return:
        mock_return.return_value = test_case
        response = client.post("/triage", json = fake)
    data = response.json()
    
    assert data['recommendation']['follow_up'] == 3
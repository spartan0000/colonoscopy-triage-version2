import pytest

from unittest.mock import AsyncMock, patch

from app import functions
from app.models.colonoscopy import ColonoscopySummary

def test_extract_structured_data(client, test_case):
    fake = {'user_query': 'test text'}

    with patch("app.functions.format_query_json", new_callable=AsyncMock) as mock_return:
        mock_return.return_value = test_case.model_dump()
        response = client.post("/triage", json = fake)

    assert response.status_code == 200

    data = response.json()

    assert data['recommendation'] is not None
    #age out rule number is 20 somewhat arbitrarily assigned
    assert data['recommendation']['follow_up'] == 20


import pytest

from fastapi.testclient import TestClient

from app.main import app

from app import functions

from app.models.colonoscopy import Colonoscopy, ColonoscopySummary, BostonBowelPrepScore, Polyp

@pytest.fixture(scope = 'session')
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope = 'function')
def test_case():
    p = Polyp(location = 'cecum',
              dysplasia = 'low_grade',
              size = 3,
              type = 'adenoma',
              resection = 'complete',
              retrieval = 'complete')
    bbps = BostonBowelPrepScore(
        total = 9,
        right = 3,
        transverse = 3,
        left = 3
    )

    c = Colonoscopy(
        date = '2025-5-5',
        number_of_polyps=1,
        cecum_reached = True,
        bostonBowelPrepScore=bbps,
        polyps = [p]
    )

    final = ColonoscopySummary(
        patient_name = 'bob',
        patient_NHI = 'ABC1234',
        patient_age = 100,
        indication = 'unknown',
        colonoscopy = [c]
    )

    return final
import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "Art Class": {
        "description": "Explore painting, drawing, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "noah@mergington.edu"],
    },
    "Drama Club": {
        "description": "Rehearse and perform plays, improv, and stagecraft",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["oliver@mergington.edu", "mia@mergington.edu"],
    },
    "Debate Team": {
        "description": "Practice public speaking and competitive debating",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["lucas@mergington.edu", "amelia@mergington.edu"],
    },
    "Science Club": {
        "description": "Investigate experiments and science fair projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["jack@mergington.edu", "harper@mergington.edu"],
    },
}


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_defined_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert "michael@mergington.edu" in payload["Chess Club"]["participants"]


def test_signup_for_activity_adds_participant():
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up test@example.com for Chess Club"}
    assert "test@example.com" in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400


def test_unregister_from_activity_removes_participant():
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_participant_returns_400():
    response = client.delete("/activities/Chess%20Club/signup?email=unknown@example.com")
    assert response.status_code == 400

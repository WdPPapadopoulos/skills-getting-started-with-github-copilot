def test_get_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities_returns_all_activities_with_expected_shape(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert len(payload) == 9
    assert "Chess Club" in payload
    assert set(payload["Chess Club"].keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }


def test_signup_for_activity_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"



def test_signup_for_activity_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_returns_404_when_activity_does_not_exist(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "new.student@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_removes_existing_participant(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "james@mergington.edu"
    path = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(path, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_participant_returns_404_when_activity_does_not_exist(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "james@mergington.edu"
    path = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_returns_404_when_participant_is_missing(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "missing@mergington.edu"
    path = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

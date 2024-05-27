import pytest
from django.urls import reverse


def assert_response_status(response, expected_status):
    assert response.status_code == expected_status


def assert_redirect_url(response, expected_url):
    assert response.url == expected_url


def assert_user_authenticated(response, expected_authentication):
    assert response.context["user"].is_authenticated == expected_authentication


@pytest.mark.django_db
def test_login_success(client, test_create_user):
    user, password = test_create_user

    login_url = reverse("accounts:login")
    response = client.get(login_url)
    assert_response_status(response, 200)

    response = client.post(login_url, {"username": user.username, "password": password})
    assert_response_status(response, 302)
    assert_redirect_url(response, reverse("accounts:top"))

    response = client.get(reverse("accounts:top"))
    assert_response_status(response, 200)
    assert_user_authenticated(response, True)


@pytest.mark.django_db
def test_login_failure(client, test_create_user):
    user, password = test_create_user

    login_url = reverse("accounts:login")
    response = client.get(login_url)
    assert_response_status(response, 200)

    response = client.post(
        login_url, {"username": user.username, "password": password + "bad"}
    )
    assert_response_status(response, 200)
    assert_user_authenticated(response, False)

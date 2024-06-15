import pytest
from django.urls import reverse

from tests.assert_utils import (
    assert_redirect_url,
    assert_response_status,
    assert_user_authenticated,
)


@pytest.mark.django_db
def test_login_success(client, test_create_user):
    """
    Test the login functionality of the application.

    This test verifies that a user can successfully log in with valid credentials.
    - It checks that the login page can be accessed.
    - It posts valid login credentials
        and checks for a successful redirect to the top page.
    - It verifies that the user is authenticated and can access the top page.
    """
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
    """
    Test the login functionality with invalid credentials.

    This test verifies that a user cannot log in with invalid credentials.
    - It checks that the login page can be accessed.
    - It posts invalid login credentials and ensures the login attempt fails.
    - It verifies that the user remains unauthenticated.
    """
    user, password = test_create_user

    login_url = reverse("accounts:login")
    response = client.get(login_url)
    assert_response_status(response, 200)

    response = client.post(
        login_url, {"username": user.username, "password": password + "bad"}
    )
    assert_response_status(response, 200)
    assert_user_authenticated(response, False)

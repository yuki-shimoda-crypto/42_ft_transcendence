import pytest
from django.urls import reverse

from tests.assert_utils import assert_response_status, assert_user_authenticated


@pytest.mark.django_db
def test_logout_success(client, test_create_user):
    """
    Test the logout functionality of the application.

    This test verifies that a user can successfully log in and log out.
    - First, it logs in a user and checks that
        the user is authenticated and can access the top page.
    - Then, it logs out the user and checks that
        the user is no longer authenticated and is redirected to the logout done page.
    """
    user, password = test_create_user

    client.login(username=user.username, password=password)
    response = client.get(reverse("accounts:top"))
    assert_response_status(response, 200)
    assert_user_authenticated(response, True)

    logout_url = reverse("accounts:logout")
    response = client.post(logout_url)
    assert_response_status(response, 200)

    response = client.get(reverse("accounts:top"))
    assert_response_status(response, 200)
    assert_user_authenticated(response, False)

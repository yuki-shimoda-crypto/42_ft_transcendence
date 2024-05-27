import pytest
from django.urls import reverse

from tests.assert_utils import assert_response_status, assert_user_authenticated


@pytest.mark.django_db
def test_logout_success(client, test_create_user):
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

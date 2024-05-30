import pytest
from accounts.models import CustomUser
from django.urls import reverse


@pytest.fixture
def test_create_user(db):
    username = "testuser"
    password = "testpassword"
    user = CustomUser.objects.create_user(username=username, password=password)
    return user, password


@pytest.fixture
def signup_url():
    return reverse("accounts:signup")


@pytest.fixture
def signup_done_url():
    return reverse("accounts:signup_done")

import pytest
from django.contrib.auth.models import User


@pytest.fixture
def test_create_user(db):
    username = "testuser"
    password = "testpassword"
    user = User.objects.create_user(username=username, password=password)
    return user, password

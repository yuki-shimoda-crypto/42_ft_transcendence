import pytest
from accounts.models import CustomUser


@pytest.fixture
def test_create_user(db):
    username = "testuser"
    password = "testpassword"
    user = CustomUser.objects.create_user(username=username, password=password)
    return user, password

import pytest
from accounts.models import CustomUser
from django.urls import reverse


@pytest.fixture
def create_users(db):
    """Fixture to create test users.

    This fixture creates two test users for use in the friend functionality tests.
    """
    user1 = CustomUser.objects.create_user(username="user1", password="password1")
    user2 = CustomUser.objects.create_user(username="user2", password="password2")
    return user1, user2


@pytest.mark.django_db
def test_add_friend(client, create_users):
    """Test adding a friend and verifying on the my_page view.

    This test ensures
    that after adding a friend, the friend is displayed on the my_page view.

    Args:
        client (Client): The test client.
        create_users (tuple): A tuple containing two test users.
    """
    user1, user2 = create_users
    client.login(username=user1.username, password="password1")

    profile_url = reverse("profile", kwargs={"username": user2.username})
    response = client.get(profile_url)
    assert response.status_code == 200
    assert "フレンド登録" in response.content.decode()

    friend_url = reverse("friend", kwargs={"username": user2.username})
    response = client.post(friend_url)
    assert response.status_code == 302

    my_page_url = reverse("accounts:my_page", kwargs={"pk": user1.pk})
    response = client.get(my_page_url)
    assert response.status_code == 200
    assert user2.username in response.content.decode()


@pytest.mark.django_db
def test_remove_friend(client, create_users):
    """Test removing a user from the friend list.

    This test ensures
    that a user can successfully remove another user from their friend list.

    Args:
        client (Client): The test client.
        create_users (tuple): A tuple containing two test users.
    """
    user1, user2 = create_users
    user1.friend_users.add(user2)
    client.login(username=user1.username, password="password1")

    url = reverse("friend", kwargs={"username": user2.username})
    response = client.post(url)

    assert response.status_code == 302
    assert user2 not in user1.friend_users.all()

    my_page_url = reverse("accounts:my_page", kwargs={"pk": user1.pk})
    response = client.get(my_page_url)
    assert response.status_code == 200
    assert user2.username not in response.content.decode()


@pytest.mark.django_db
def test_toggle_friend(client, create_users):
    """Test toggling a user in the friend list.

    This test ensures that a user can toggle the friend status of another user
    (i.e., add if not already a friend, or remove if already a friend).

    Args:
        client (Client): The test client.
        create_users (tuple): A tuple containing two test users.
    """
    user1, user2 = create_users
    client.login(username=user1.username, password="password1")

    url = reverse("friend", kwargs={"username": user2.username})

    response = client.post(url)
    assert response.status_code == 302

    my_page_url = reverse("accounts:my_page", kwargs={"pk": user1.pk})
    response = client.get(my_page_url)
    assert response.status_code == 200
    assert user2.username in response.content.decode()
    assert user2 in user1.friend_users.all()

    response = client.post(url)
    assert response.status_code == 302

    my_page_url = reverse("accounts:my_page", kwargs={"pk": user1.pk})
    response = client.get(my_page_url)
    assert response.status_code == 200
    assert user2.username not in response.content.decode()
    assert user2 not in user1.friend_users.all()

import pytest
from django.urls import reverse
from accounts.models import CustomUser


@pytest.mark.django_db
def test_mypage_access(
    client,
):
    user = CustomUser.objects.create_user(username="testuser", password="testpassword")

    mypage_url = reverse("accounts:my_page", kwargs={"pk": user.pk})

    response = client.get(mypage_url)
    assert response.status_code == 403

    client.login(username="testuser", password="testpassword")
    response = client.get(mypage_url)
    assert response.status_code == 200
    assert "testuser" in response.content.decode()


@pytest.mark.django_db
def test_mypage_access_denied(client):
    user = CustomUser.objects.create_user(username="testuser", password="testpassword")
    ohter_user = CustomUser.objects.create_user(
        username="otheruser", password="testpassword"
    )

    mypage_url = reverse("accounts:my_page", kwargs={"pk": user.pk})

    client.login(username="otheruser", password="testpassword")
    response = client.get(mypage_url)
    assert response.status_code == 403

    response = client.get(reverse("accounts:my_page", kwargs={"pk": ohter_user.pk}))
    assert response.status_code == 200
    assert "otheruser" in response.content.decode()

import pytest
from accounts.models import CustomUser
from django.urls import reverse


@pytest.mark.django_db
def test_signup_get(client, signup_url):
    response = client.get(signup_url)
    assert response.status_code == 200
    assert "form" in response.context
    assert "Sign Up" in response.content.decode()


@pytest.mark.django_db
def test_signup_post_valid(client, signup_url, signup_done_url):
    response = client.post(
        signup_url,
        {
            "username": "newuser",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        },
    )
    assert response.status_code == 302
    assert response.url == signup_done_url
    assert CustomUser.objects.filter(username="newuser").exists()

    login_url = reverse("accounts:login")
    response = client.post(
        login_url, {"username": "newuser", "password": "ComplexPassword123!"}
    )
    assert response.status_code == 302
    assert response.url == reverse("accounts:top")

    response = client.get(reverse("accounts:top"))
    assert response.status_code == 200
    assert response.context["user"].is_authenticated is True


@pytest.mark.django_db
def test_signup_post_invalid_password_mismatch(client, signup_url):
    response = client.post(
        signup_url,
        {
            "username": "newuser",
            "password1": "ComplexPassword123!",
            "password2": "DifferentPassword123!",
        },
    )
    assert response.status_code == 200
    assert "form" in response.context
    assert "確認用パスワードが一致しません。" in response.content.decode()
    assert not CustomUser.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_signup_post_missing_username(client, signup_url):
    response = client.post(
        signup_url,
        {
            "username": "",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        },
    )
    assert response.status_code == 200
    assert "form" in response.context
    assert not CustomUser.objects.filter(username="").exists()


@pytest.mark.django_db
def test_signup_post_same_username(client, signup_url, signup_done_url):
    response = client.post(
        signup_url,
        {
            "username": "newuser",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        },
    )
    assert response.status_code == 302
    assert response.url == signup_done_url
    assert CustomUser.objects.filter(username="newuser").exists()
    response = client.post(
        signup_url,
        {
            "username": "newuser",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        },
    )
    assert response.status_code == 200
    assert "form" in response.context
    assert "同じユーザー名が既に登録済みです。" in response.content.decode()

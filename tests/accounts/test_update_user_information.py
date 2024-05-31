import pytest
from accounts.models import CustomUser
from accounts.utils import generate_default_profile_image
from django.urls import reverse


@pytest.mark.django_db
def test_username_update_get(client, test_create_user):
    """
    Test the GET request for updating the username view.

    This test verifies that the username update page can be accessed
    correctly.
    - It checks that the page cannot be accessed without logging in.
    - It logs in with valid credentials and checks for successful access to the page.
    - It verifies that the page contains the process name "Update Username".
    """
    user, password = test_create_user

    url = reverse("accounts:username_update", kwargs={"pk": user.pk})

    response = client.get(url)
    assert response.status_code == 403

    client.login(username=user.username, password=password)
    response = client.get(url)
    assert response.status_code == 200
    assert "Update Username" in response.content.decode()


@pytest.mark.django_db
def test_username_update_post_valid(client, test_create_user):
    """
    Test the POST request for updating the username view.

    This test verifies that a user can successfully update their username.
    - It logs in with valid credentials.
    - It posts a new valid username and checks for a successful redirect.
    - It verifies that the username has been updated in the database.
    """
    user, password = test_create_user

    url = reverse("accounts:username_update", kwargs={"pk": user.pk})

    client.login(username=user.username, password=password)
    new_username = "updateduser"
    response = client.post(url, {"username": new_username})
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.username == new_username


@pytest.mark.django_db
def test_username_update_post_same_username(client, test_create_user):
    """
    Test the POST request for updating the username view with an existing username.

    This test verifies that attempting to update the username to an already
    existing username results in a validation error.
    - It creates an existing user with a specific username.
    - It logs in with valid credentials.
    - It attempts to update the username to the existing one
        and checks for an error message.
    """
    existinguser = CustomUser.objects.create_user(
        username="updateduser", password="passwordNewuser"
    )
    user, password = test_create_user

    url = reverse("accounts:username_update", kwargs={"pk": user.pk})

    client.login(username=user.username, password=password)
    response = client.get(reverse("accounts:my_page", kwargs={"pk": user.pk}))
    assert response.status_code == 200
    assert user.username in response.content.decode()

    response = client.post(url, {"username": existinguser})
    assert "同じユーザー名が既に登録済みです。" in response.content.decode()


@pytest.mark.django_db
def test_profile_image_update_get(client, test_create_user):
    """
    Test the GET request for updating the profile image view.

    This test verifies that the profile image update page can be accessed
    correctly.
    - It checks that the page cannot be accessed without logging in.
    - It logs in with valid credentials and checks for successful access to the page.
    - It verifies that the page contains the process name "Update Profile Image".
    """
    user, password = test_create_user

    url = reverse("accounts:profile_image_update", kwargs={"pk": user.pk})

    response = client.get(url)
    assert response.status_code == 403

    client.login(username=user.username, password=password)
    response = client.get(url)
    assert response.status_code == 200
    assert "Update Profile Image" in response.content.decode()


@pytest.mark.django_db
def test_profile_image_update_post_valid(client, test_create_user):
    """
    Test the POST request for updating the profile image view.

    This test verifies that a user can successfully update their profile image.
    - It logs in with valid credentials.
    - It posts a new profile image and checks for a successful redirect.
    """
    user, password = test_create_user

    url = reverse("accounts:profile_image_update", kwargs={"pk": user.pk})

    client.login(username=user.username, password=password)
    image = generate_default_profile_image(user.username)
    response = client.post(url, {"profile_image": image})
    assert response.status_code == 302


@pytest.mark.django_db
def test_password_change_get_success(client, test_create_user):
    """
    Test the GET request for changing the password view.

    This test verifies that the password change page can be accessed correctly.
    - It checks that the page cannot be accessed without logging in.
    - It logs in with valid credentials and checks for successful access to the page.
    - It verifies that the page contains the process name "Change Password".
    """
    user, password = test_create_user

    url = reverse("accounts:password_change")

    response = client.get(url)
    assert response.status_code == 302

    client.login(username=user.username, password=password)
    response = client.get(url)
    assert response.status_code == 200
    assert "Change Password" in response.content.decode()


@pytest.mark.django_db
def test_password_change_post_valid(client, test_create_user):
    """
    Test the POST request for changing the password view.

    This test verifies that a user can successfully change their password.
    - It logs in with valid credentials.
    - It posts the old and new passwords and checks for a successful redirect.
    - It verifies that the password has been updated in the database.
    """
    user, password = test_create_user

    url = reverse("accounts:password_change")

    client.login(username=user.username, password=password)
    new_password = "newtestpassword"
    response = client.post(
        url,
        {
            "old_password": password,
            "new_password1": new_password,
            "new_password2": new_password,
        },
    )
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.check_password(new_password)


@pytest.mark.django_db
def test_password_change_post_invalid_old_password(client, test_create_user):
    """
    Test the POST request for changing the password view with an invalid old password.

    This test verifies that attempting to change the password with an invalid
    old password results in a validation error.
    - It logs in with valid credentials.
    - It posts an incorrect old password and checks for an error message.
    - It verifies that the password has not been changed in the database.
    """
    user, password = test_create_user

    url = reverse("accounts:password_change")

    client.login(username=user.username, password=password)
    new_password = "newtestpassword"
    response = client.post(
        url,
        {
            "old_password": password + "invalid",
            "new_password1": new_password,
            "new_password2": new_password,
        },
    )
    assert response.status_code == 200
    assert "元のパスワードが間違っています。" in response.content.decode()
    user.refresh_from_db()
    assert user.check_password(password)


@pytest.mark.django_db
def test_password_change_post_invalid_new_password(client, test_create_user):
    """
    Test the POST request for changing the password view
    with non-matching new passwords.

    This test verifies that attempting to change the password with non-matching
    new passwords results in a validation error.
    - It logs in with valid credentials.
    - It posts non-matching new passwords and checks for an error message.
    - It verifies that the password has not been changed in the database.
    """
    user, password = test_create_user

    url = reverse("accounts:password_change")

    client.login(username=user.username, password=password)
    new_password = "newtestpassword"
    response = client.post(
        url,
        {
            "old_password": password,
            "new_password1": new_password,
            "new_password2": new_password + "invalid",
        },
    )
    assert response.status_code == 200
    assert "確認用パスワードが一致しません。" in response.content.decode()
    user.refresh_from_db()
    assert user.check_password(password)

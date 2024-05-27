def assert_response_status(response, expected_status):
    assert response.status_code == expected_status

def assert_redirect_url(response, expected_url):
    assert response.url == expected_url

def assert_user_authenticated(response, expected_authentication):
    assert response.context['user'].is_authenticated == expected_authentication

from src.services.auth import Authentication


def test_create_access_token():
    data = {"user_id": 1}

    jwt_token = Authentication.create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    decode_token = Authentication.decode_token(jwt_token)

    assert decode_token["user_id"] == 1

async def test_get_profile(auth_ac_customer):
    responses = await auth_ac_customer.get("/profiles/1")

    assert responses.status_code == 200
    assert "id" in responses.json()
    assert "username" in responses.json()
    assert "email" in responses.json()
    assert "first_name" in responses.json()
    assert "last_name" in responses.json()
    assert "middle_name" in responses.json()
    assert "rating" in responses.json()
    assert "role" in responses.json()
    assert "created_at" in responses.json()


async def test_get_user_review(auth_ac_customer):
    responses = await auth_ac_customer.get("/profiles/1/reviews")

    assert responses.status_code == 200

async def test_logout(auth_ac_customer):
    response = await auth_ac_customer.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

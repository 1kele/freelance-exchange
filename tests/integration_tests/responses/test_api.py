
async def test_get_all_my_responses(auth_ac_freelancer):
    response = await auth_ac_freelancer.get("/response/my")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"


async def test_respond_to_order(auth_ac_freelancer):
    response = await auth_ac_freelancer.post(
        "/orders/2/responses",
        json={
            "cover_letter": "Я готов",
            "proposed_price": 5000
        }
    )
    response2 = await auth_ac_freelancer.post(
        "/orders/3/responses",
        json={
            "cover_letter": "Я ready",
            "proposed_price": 50000
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response2.status_code == 200
    assert response2.json()["status"] == "OK"


async def test_accept_response(auth_ac_customer):
    response = await auth_ac_customer.patch(
        "/orders/response/1/accept"
    )

    response_second = await auth_ac_customer.patch(
        "/orders/response/2/accept"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response_second.status_code == 200
    assert response_second.json()["status"] == "OK"


async def test_complete_order(auth_ac_freelancer):
    response = await auth_ac_freelancer.patch(
        "/orders/2/complete"
    )
    response_second = await auth_ac_freelancer.patch(
        "/orders/3/complete"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response_second.status_code == 200
    assert response_second.json()["status"] == "OK"


async def test_reject_response(auth_ac_customer):
    response = await auth_ac_customer.patch(
        "/orders/response/2/rejected"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
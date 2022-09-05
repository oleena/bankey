import pytest
import random
import string

from decimal import Decimal
from rest_framework.test import APIClient

import django

django.setup()

from core.models import CustomUser  # NOQA


def string_generator(size=8, chars=string.ascii_lowercase):
    return "".join(random.choice(chars) for _ in range(size))


@pytest.fixture(scope="session")
def user():
    username = string_generator(chars=string.ascii_lowercase)
    password = string_generator(chars=string.ascii_lowercase + string.digits)
    user = CustomUser.objects.create_user(username=username, password=password)
    user.save()
    yield username, password
    CustomUser.objects.filter(id=user.pk).delete()


@pytest.fixture
def client():
    return APIClient(SERVER_NAME="localhost")


@pytest.fixture
def login(client, user):
    username, password = user
    response = client.post(
        "/accounts/login/",
        data={"username": username, "password": password},
    )
    assert 302 == response.status_code, "Should be redirecting to User's balance page"
    return response


def test_login(login):
    assert 302 == login.status_code


def test_dashboard(login, client):
    resp = client.get("/dashboard/")
    assert 200 == resp.status_code


def test_register(client):
    username = string_generator()
    response = client.post(
        "/signup/",
        data={"username": username, "password1": "1234haslo"},
    )
    assert response.status_code == 302, "Error, should be redirecting to Login Page"


def test_transfer(client, login, user):
    username = string_generator()
    response = client.post(
        "/signup/",
        data={"username": username, "password1": "1234haslo"},
    )
    assert response.status_code == 302

    response = client.get("/balance/")
    balance_before = response.data["balance"]

    response = client.post(
        "/transfer/",
        data={"recipient": username, "amount": Decimal("6.99")},
    )
    assert response.data["status"] == "OK"

    response = client.get("/balance/")
    balance_now = response.data["balance"]
    assert balance_now == balance_before - Decimal("6.99")


def test_balance(login, client):
    resp = client.get("/balance/")
    assert 200 == resp.status_code

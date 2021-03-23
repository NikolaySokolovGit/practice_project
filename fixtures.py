import pytest

from utils import api_create_client, api_create_order


@pytest.fixture(scope='function')
def client():
    def create_client(name, surname, phone):
        client_id = api_create_client(name, surname, phone)
        return client_id
    return create_client


@pytest.fixture(scope='function')
def order():
    def create_order(client_id, address, phone, item_id, price, quantity):
        order_id, order_num = api_create_order(client_id, address, phone, item_id, price, quantity)
        return order_id, order_num
    return create_order

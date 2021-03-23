import json
from datetime import datetime, timedelta

import pytest

from utils import api_purchase_by_client


class TestPurchase:
    @pytest.mark.parametrize('name, surname, phone, address, item_id, price, quantity',
                             [pytest.param('Ivan', 'Ivanov', '+1 123 456 78 90', 'Moscow', 'item_1', 100500, 1)],
                             )
    def test_one_item_exists(self, client, order, name, surname, phone, address, item_id, price, quantity):
        """
        Кейс, когда клиент покупал один вид айтема
        :param name: Имя клиента
        :param surname: Фамилия клиента
        :param phone: Номер телефона клиента
        :param address: Адрес доставки
        :param phone: Номер телефона получателя
        :param item_id: id товара
        :param price: Цена единицы продукта
        :param quantity: Количество единиц продукта
        """
        client_id = client(name, surname, phone)
        order_id, order_num = order(client_id, address, phone, item_id, price, quantity)
        dt = datetime.now()
        purchase = api_purchase_by_client(client_id, item_id)
        assert str(purchase.status_code).startswith('2'), f'Код статуса {purchase.status_code}'
        purchase_json = json.loads(purchase.text)
        item = purchase_json['items'][0]
        assert item['purchased'], 'Продукт не отмечен как purchased'
        assert item['last_order_number'] == order_num, 'Неверный номер последнего заказа'
        assert dt - timedelta(seconds=10) <= datetime.fromisoformat(item['last_purchase_date'][:-1]) <= dt, \
            'Неверная дата последнего заказа'
        assert item['purchase_count'] == 1, 'Неверное число покупок'

    @pytest.mark.parametrize('name, surname, phone, address, item1_id, price, quantity, item2_id',
                             [pytest.param('Sidor', 'Sidorov', '+2 123 456 78 90', 'Moscow', 'item_1', 100500, 1,
                                           'item_2')],
                             )
    def test_multiple_items_exist(self, client, order, name, surname, phone, address, item1_id, price, quantity,
                                  item2_id):
        """
        Кейс, когда клиент покупал несколько (два) видов айтемов
        :param name: Имя клиента
        :param surname: Фамилия клиента
        :param phone: Номер телефона клиента
        :param address: Адрес доставки
        :param phone: Номер телефона получателя
        :param item1_id: id товара 1
        :param price: Цена единицы продукта
        :param quantity: Количество единиц продукта
        :param item2_id: id товара 2
        """
        client_id = client(name, surname, phone)
        order_id1, order_num1 = order(client_id, address, phone, item1_id, price, quantity)
        order_id2, order_num2 = order(client_id, address, phone, item2_id, price, quantity)
        order_nums = {1: order_num1, 2: order_num2}
        dt = datetime.now()
        purchase = api_purchase_by_client(client_id, item1_id, item2_id)
        assert str(purchase.status_code).startswith('2'), f'Код статуса {purchase.status_code}'
        purchase_json = json.loads(purchase.text)
        item1, item2 = purchase_json['items']
        for num, item in enumerate((item1, item2), 1):
            assert item['purchased'], f'Продукт {num} не отмечен как purchased'
            assert item['last_order_number'] == order_nums[num], f'Неверный номер последнего заказа продукта {num}'
            assert dt - timedelta(seconds=10) <= datetime.fromisoformat(item1['last_purchase_date'][:-1]) <= dt, \
                f'Неверная дата последнего заказа продукта {num}'
            assert item['purchase_count'] == quantity, f'Неверное число покупок продукта {num}'

    @pytest.mark.parametrize('name, surname, phone, item_id',
                             [pytest.param('Piotr', 'Petrov', '+3 123 456 78 90', 'nonexistingitemid')],
                             )
    def test_item_not_exist(self, client, name, surname, phone, item_id):
        """
        Кейс, когда указан item_id, который клиент не покупал
        :param name: Имя клиента
        :param surname: Фамилия клиента
        :param phone: Номер телефона клиента
        :param item_id: id товара
        """
        client_id = client(name, surname, phone)
        purchase = api_purchase_by_client(client_id, item_id)
        assert str(purchase.status_code).startswith('2'), f'Код статуса {purchase.status_code}'
        purchase_json = json.loads(purchase.text)
        item = purchase_json['items'][0]
        assert not item['purchased'], f'Продукт отмечен как purchased'

    def test_client_doesnt_exist(self):
        """
        Кейс, когда указан несуществующий client_id
        """
        purchase = api_purchase_by_client('nonexistingclientid', 'nonexistingitemid')
        assert purchase.status_code == 404, f'Код статуса {purchase.status_code} вместо 404'
        assert purchase.text == 'Unexisting client id message text', f'Некорректное сообщение ошибки"{purchase.text}"'



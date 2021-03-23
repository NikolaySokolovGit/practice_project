import requests
import json


def api_create_client(name: str, surname: str, phone: str) -> str:
    """
    Отправляет запрос к api для создания ресурса клиента
    :param name: Имя клиента
    :param surname: Фамилия клиента
    :param phone: Номер телефона клиента
    :return: client_id
    """
    data = {
        "name": f'{name}',
        "surname": f'{surname}',
        "phone": f'{phone}'
    }
    response = requests.post('service/v1/client/create', json=data)
    client_id = json.loads(response.text)['client_id']
    return str(client_id)


def api_create_order(client_id: str, address: str, phone: str, item_id: str, price: float, quantity: int) -> tuple:
    """
    Отправляет запрос к api для создания ресурса заказа
    :param client_id: id клиента
    :param address: Адрес доставки
    :param phone: Номер телефона получателя
    :param item_id: id товара
    :param price: Цена единицы продукта
    :param quantity: Количество единиц продукта
    :return: (order_id, order_num)
    """
    data = {
        "client_id": client_id,
        "address": address,
        "phone": phone,
        "items": [
            {
                "item_id": item_id,
                "price_id": price,
            }
        ],
        "quantity": quantity
    }
    response = requests.post('service/v1/order/create', json=data)
    order_id = json.loads(response.text)['order_id']
    order_num = json.loads(response.text)['order_number']
    return str(order_id), str(order_num)


def api_purchase_by_client(client_id: str, *item_ids: str):
    """
    Отправляет запрос к api для получения информации о приобретении клиентом конкретных item_id
    :param client_id: id клиента
    :param item_ids: id продуктов
    :return: json с информацией о последних заказах клиента с указанными item_id и количеством для каждого item_id
    """
    data = {
        "client_id": client_id,
        "item_ids": [item_id for item_id in item_ids]
    }
    response = requests.post('service/v1/item/purchase/by-client', json=data)
    return response

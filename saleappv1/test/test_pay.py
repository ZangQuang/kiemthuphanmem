from test.test_base import test_client, test_app

from eapp.models import User, Product, Receipt, ReceiptDetails

def test_pay_sucess(test_client, mocker):
    class Fakeuser:
        is_authenticated = True

    mocker.patch('flask_login.utils._get_user', return_value=Fakeuser())

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "2": {
                "id": "2",
                "name": "aaaa",
                "price": 50,
                "quantity": 2
            }
        }

    mock_receipt = mocker.patch('eapp.dao.add_receipt')

    res = test_client.post('api/pay')

    data = res.get_json()

    assert data['status'] == 200

    with test_client.session_transaction() as sess:
        assert 'cart' not in sess

    mock_receipt.assert_called_once()


def test_pay_exception(test_client, mocker):
    class Fakeuser:
        is_authenticated = True

    mocker.patch('flask_login.utils._get_user', return_value=Fakeuser())

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "2": {
                "id": "2",
                "name": "aaaa",
                "price": 50,
                "quantity": 2
            }
        }

    mock_receipt = mocker.patch('eapp.dao.add_receipt', side_effect = Exception("DB Error"))

    res = test_client.post('api/pay')

    data = res.get_json()

    assert data['status'] == 400
    assert data['err_msg'] == "DB Error"

    with test_client.session_transaction() as sess:
        assert 'cart' in sess

    mock_receipt.assert_called_once()


def test_all(test_client):

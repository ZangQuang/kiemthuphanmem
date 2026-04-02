from test.test_base import test_client, test_app

def test_add_to_cart(test_client):
    res = test_client.post('/api/carts', json={
        'id': 1,
        'name': 'aaa',
        'price': 50
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 1
    assert data['total_amount'] == 50

def test_add_increase_item(test_client):
    test_client.post('/api/carts', json={
        'id': 1,
        'name': 'aaa',
        'price': 50
    })

    test_client.post('/api/carts', json={
        'id': 1,
        'name': 'aaa',
        'price': 50
    })

    res = test_client.post('/api/carts', json={
        'id': 2,
        'name': 'aaa',
        'price': 50
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 3
    assert data['total_amount'] == 150

    with test_client.session_transaction() as sess:
        assert 'cart' in sess
        assert len(sess['cart']) == 2
        assert sess['cart']['1']['quantity'] == 2

def test_add_exiting(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "2": {
                "id": "2",
                "name": "aaaa",
                "price": 50,
                "quantity": 2
            }
        }

    res = test_client.post('/api/carts', json={
        'id': 2,
        'name': 'aaaa',
        'price': 50
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 3
    assert data['total_amount'] == 150

    with test_client.session_transaction() as sess:
        assert 'cart' in sess
        assert len(sess['cart']) == 1
        assert sess['cart']['2']['quantity'] == 3
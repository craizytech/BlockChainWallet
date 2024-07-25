def test_create_wallet(client, auth_headers):
    response = client.post('/wallet/create', json={
        'user_id': 1,
        'wallet_address': '0x12345',
        'network': 'Ethereum'
    }, headers=auth_headers)
    assert response.status_code == 201

def test_delete_wallet(client, auth_headers):
    response = client.post('/wallet/delete', json={
        'wallet_id': 1
    }, headers=auth_headers)
    assert response.status_code == 200

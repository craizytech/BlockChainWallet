def test_create_dashboard(client, auth_headers):
    response = client.post('/dashboard/create', json={
        'user_id': 1,
        'name': 'My Dashboard',
        'type': 'ETH'
    }, headers=auth_headers)
    assert response.status_code == 201

def test_delete_dashboard(client, auth_headers):
    response = client.post('/dashboard/delete', json={
        'dashboard_id': 1
    }, headers=auth_headers)
    assert response.status_code == 200

def test_show_transactions(client, auth_headers):
    response = client.get('/dashboard/transactions', query_string={
        'wallet_id': 1,
        'network': 'Ethereum'
    }, headers=auth_headers)
    assert response.status_code == 200

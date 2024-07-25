def test_start_monitoring(client):
    response = client.post('/monitoring/start')
    assert response.data == b"Monitoring started"

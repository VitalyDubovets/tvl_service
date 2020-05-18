import pytest

from rest_framework.test import APIClient


class TestLinksCreateAPI:

    def zadd_with_unix_time_mock(self, key, values):
        return True

    def test_successfully_create_links(self, monkeypatch):
        from core.redis_db import RedisDB

        data = {'links': ['example.com', 'example11.com']}

        monkeypatch.setattr(RedisDB, 'zadd_with_unix_time', value=self.zadd_with_unix_time_mock)
        client = APIClient()
        response = client.post('/api/v1/links/visited_links', data=data, format='json')
        assert response.status_code == 201

    def test_invalid_data(self, monkeypatch):
        from core.redis_db import RedisDB

        data = {}

        monkeypatch.setattr(RedisDB, 'zadd_with_unix_time', value=self.zadd_with_unix_time_mock)
        client = APIClient()
        response = client.post('/api/v1/links/visited_links', data=data, format='json')
        assert response.status_code == 400


class TestLinksGetAPI:
    def mock_zrange_unix_time(self, key, min, max):
        return ['example.com/asdasdf', 'example11.com/asdas']

    def test_valid_get_request(self, monkeypatch):
        from core.redis_db import RedisDB

        monkeypatch.setattr(RedisDB, 'zrange_by_unix_time', value=self.mock_zrange_unix_time)
        client = APIClient()
        response = client.get('/api/v1/links/visited_domains?from=1400000000&to=1600000000')
        assert response.status_code == 200

    def test_invalid_get_params(self, monkeypatch):
        from core.redis_db import RedisDB

        monkeypatch.setattr(RedisDB, 'zrange_by_unix_time', value=self.mock_zrange_unix_time)
        client = APIClient()
        response = client.get('/api/v1/links/visited_domains?from=kek&to=kek')
        assert response.status_code == 400

    def test_no_domains(self, monkeypatch):
        from core.redis_db import RedisDB

        def mock_zrange_without_data(self, key, min=0, max=-1):
            return []

        monkeypatch.setattr(RedisDB, 'zrange_decoded', value=mock_zrange_without_data)
        client = APIClient()
        response = client.get('/api/v1/links/visited_domains')
        assert response.status_code == 404

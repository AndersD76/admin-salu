"""Tests for public endpoints."""


class TestPublicEndpoints:
    def test_root(self, client):
        r = client.get("/")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "running"
        assert "name" in data
        assert "version" in data

    def test_health(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert "status" in data
        assert "database" in data

    def test_docs(self, client):
        r = client.get("/docs")
        assert r.status_code == 200

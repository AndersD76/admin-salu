"""Tests for authentication endpoints."""


class TestLogin:
    def test_login_success(self, client, admin_user):
        r = client.post(
            "/api/auth/login",
            json={"email": "admin@test.com", "password": "admin123"},
        )
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "admin@test.com"
        assert data["user"]["role"] == "ADMIN"
        # Password must NOT be in response
        assert "password" not in data["user"]

    def test_login_wrong_password(self, client, admin_user):
        r = client.post(
            "/api/auth/login",
            json={"email": "admin@test.com", "password": "wrong"},
        )
        assert r.status_code == 401

    def test_login_nonexistent_user(self, client):
        r = client.post(
            "/api/auth/login",
            json={
                "email": "nobody@test.com",
                "password": "test",
            },
        )
        assert r.status_code == 401

    def test_login_non_admin_rejected(self, client, regular_user):
        r = client.post(
            "/api/auth/login",
            json={"email": "user@test.com", "password": "user123"},
        )
        assert r.status_code == 403
        assert "Admin access only" in r.json()["detail"]

    def test_login_invalid_email_format(self, client):
        r = client.post(
            "/api/auth/login",
            json={"email": "notanemail", "password": "test"},
        )
        assert r.status_code == 422

    def test_login_missing_body(self, client):
        r = client.post("/api/auth/login")
        assert r.status_code == 422

    def test_login_rate_limiting(self, client, admin_user):
        """Test that rate limiting kicks in after too many attempts."""
        for i in range(5):
            client.post(
                "/api/auth/login",
                json={
                    "email": "admin@test.com",
                    "password": "wrong",
                },
            )
        # 6th attempt should be rate limited
        r = client.post(
            "/api/auth/login",
            json={
                "email": "admin@test.com",
                "password": "admin123",
            },
        )
        assert r.status_code == 429


class TestMe:
    def test_me_success(self, client, auth_headers):
        r = client.get("/api/auth/me", headers=auth_headers)
        assert r.status_code == 200
        data = r.json()
        assert data["email"] == "admin@test.com"
        assert data["role"] == "ADMIN"
        # Password must NOT be in response
        assert "password" not in data

    def test_me_no_auth(self, client):
        r = client.get("/api/auth/me")
        assert r.status_code == 403

    def test_me_invalid_token(self, client):
        r = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid"},
        )
        assert r.status_code == 401

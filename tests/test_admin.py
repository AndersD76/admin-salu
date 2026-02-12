"""Tests for admin endpoints."""


class TestDashboard:
    def test_dashboard_success(self, client, auth_headers):
        r = client.get(
            "/api/admin/dashboard", headers=auth_headers
        )
        assert r.status_code == 200
        data = r.json()
        assert "overview" in data
        assert "properties_by_type" in data
        assert "contacts_by_status" in data
        assert "recent_contacts" in data
        assert "top_properties" in data

    def test_dashboard_no_auth(self, client):
        r = client.get("/api/admin/dashboard")
        assert r.status_code == 403


class TestUsers:
    def test_list_users(self, client, auth_headers, admin_user):
        r = client.get(
            "/api/admin/users", headers=auth_headers
        )
        assert r.status_code == 200
        data = r.json()
        assert data["total"] >= 1
        # Password must NOT be in any user
        for user in data["users"]:
            assert "password" not in user

    def test_list_users_no_auth(self, client):
        r = client.get("/api/admin/users")
        assert r.status_code == 403

    def test_list_users_filter_role(
        self, client, auth_headers, admin_user
    ):
        r = client.get(
            "/api/admin/users?role=ADMIN",
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["total"] >= 1

    def test_list_users_invalid_role(
        self, client, auth_headers
    ):
        r = client.get(
            "/api/admin/users?role=HACKER",
            headers=auth_headers,
        )
        assert r.status_code == 400
        assert "Invalid role" in r.json()["detail"]

    def test_list_users_pagination_limit(
        self, client, auth_headers
    ):
        # Limit > MAX_PAGE_LIMIT should fail
        r = client.get(
            "/api/admin/users?limit=999",
            headers=auth_headers,
        )
        assert r.status_code == 422

    def test_list_users_negative_skip(
        self, client, auth_headers
    ):
        r = client.get(
            "/api/admin/users?skip=-1",
            headers=auth_headers,
        )
        assert r.status_code == 422

    def test_get_user(
        self, client, auth_headers, regular_user
    ):
        r = client.get(
            f"/api/admin/users/{regular_user.id}",
            headers=auth_headers,
        )
        assert r.status_code == 200
        data = r.json()
        assert data["email"] == "user@test.com"
        assert "password" not in data

    def test_get_user_not_found(self, client, auth_headers):
        r = client.get(
            "/api/admin/users/nonexistent",
            headers=auth_headers,
        )
        assert r.status_code == 404

    def test_delete_user(
        self, client, auth_headers, regular_user
    ):
        r = client.delete(
            f"/api/admin/users/{regular_user.id}",
            headers=auth_headers,
        )
        assert r.status_code == 200
        # Verify deleted
        r = client.get(
            f"/api/admin/users/{regular_user.id}",
            headers=auth_headers,
        )
        assert r.status_code == 404

    def test_delete_self_prevented(
        self, client, auth_headers, admin_user
    ):
        r = client.delete(
            f"/api/admin/users/{admin_user.id}",
            headers=auth_headers,
        )
        assert r.status_code == 400
        assert "Cannot delete yourself" in r.json()["detail"]


class TestProperties:
    def test_list_properties(
        self, client, auth_headers, sample_property
    ):
        r = client.get(
            "/api/admin/properties", headers=auth_headers
        )
        assert r.status_code == 200
        data = r.json()
        assert data["total"] >= 1

    def test_list_properties_filter_active(
        self, client, auth_headers, sample_property
    ):
        r = client.get(
            "/api/admin/properties?is_active=true",
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["total"] >= 1

    def test_toggle_active(
        self, client, auth_headers, sample_property
    ):
        r = client.patch(
            f"/api/admin/properties/{sample_property.id}/toggle-active",
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["is_active"] is False

        # Toggle back
        r = client.patch(
            f"/api/admin/properties/{sample_property.id}/toggle-active",
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["is_active"] is True

    def test_toggle_featured(
        self, client, auth_headers, sample_property
    ):
        r = client.patch(
            f"/api/admin/properties/{sample_property.id}/toggle-featured",
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["is_featured"] is True

    def test_toggle_nonexistent(self, client, auth_headers):
        r = client.patch(
            "/api/admin/properties/fake/toggle-active",
            headers=auth_headers,
        )
        assert r.status_code == 404


class TestContacts:
    def test_list_contacts(
        self, client, auth_headers, sample_contact
    ):
        r = client.get(
            "/api/admin/contacts", headers=auth_headers
        )
        assert r.status_code == 200
        assert r.json()["total"] >= 1

    def test_update_contact_status_valid(
        self, client, auth_headers, sample_contact
    ):
        r = client.patch(
            f"/api/admin/contacts/{sample_contact.id}/status",
            headers=auth_headers,
            json={"status": "CONTACTED"},
        )
        assert r.status_code == 200
        assert r.json()["status"] == "CONTACTED"

    def test_update_contact_status_invalid(
        self, client, auth_headers, sample_contact
    ):
        r = client.patch(
            f"/api/admin/contacts/{sample_contact.id}/status",
            headers=auth_headers,
            json={"status": "INVALID"},
        )
        assert r.status_code == 400
        assert "Invalid status" in r.json()["detail"]

    def test_filter_contacts_invalid_status(
        self, client, auth_headers
    ):
        r = client.get(
            "/api/admin/contacts?status=INVALID",
            headers=auth_headers,
        )
        assert r.status_code == 400


class TestBrokers:
    def test_list_brokers(
        self, client, auth_headers, sample_broker
    ):
        r = client.get(
            "/api/admin/brokers", headers=auth_headers
        )
        assert r.status_code == 200
        assert r.json()["total"] >= 1

    def test_toggle_broker_active(
        self, client, auth_headers, sample_broker
    ):
        r = client.patch(
            f"/api/admin/brokers/{sample_broker.id}/toggle-active",
            headers=auth_headers,
        )
        assert r.status_code == 200
        assert r.json()["is_active"] is False

    def test_toggle_nonexistent_broker(
        self, client, auth_headers
    ):
        r = client.patch(
            "/api/admin/brokers/fake/toggle-active",
            headers=auth_headers,
        )
        assert r.status_code == 404


class TestCron:
    def test_cron_status_with_secret(self, client):
        r = client.get(
            "/api/admin/cron/status",
            headers={"X-Cron-Secret": "test-cron-secret"},
        )
        assert r.status_code == 200

    def test_cron_status_wrong_secret(self, client):
        r = client.get(
            "/api/admin/cron/status",
            headers={"X-Cron-Secret": "wrong"},
        )
        assert r.status_code == 401

    def test_cron_status_no_secret(self, client):
        r = client.get("/api/admin/cron/status")
        assert r.status_code == 401


class TestImportLogs:
    def test_import_logs(self, client, auth_headers):
        r = client.get(
            "/api/admin/import-logs", headers=auth_headers
        )
        assert r.status_code == 200
        assert "logs" in r.json()

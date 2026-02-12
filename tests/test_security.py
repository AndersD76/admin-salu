"""Tests for security utilities."""
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        password = "my-secure-password"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed)

    def test_wrong_password(self):
        hashed = get_password_hash("correct")
        assert not verify_password("wrong", hashed)

    def test_different_hashes(self):
        h1 = get_password_hash("same")
        h2 = get_password_hash("same")
        # bcrypt should produce different salts
        assert h1 != h2


class TestJWT:
    def test_create_and_decode(self):
        token = create_access_token(data={"sub": "user-123"})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "user-123"
        assert "exp" in payload

    def test_invalid_token(self):
        result = decode_access_token("invalid-token")
        assert result is None

    def test_sub_must_be_string(self):
        # Ensure we always pass string sub
        token = create_access_token(data={"sub": "123"})
        payload = decode_access_token(token)
        assert payload["sub"] == "123"

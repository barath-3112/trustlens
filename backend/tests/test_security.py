from app.security import create_token, decode_token, hash_password, verify_password
def test_password_hashing_and_token():
    hashed=hash_password("correct-horse-battery-staple")
    assert hashed != "correct-horse-battery-staple" and verify_password("correct-horse-battery-staple",hashed)
    assert decode_token(create_token("abc")) == "abc"

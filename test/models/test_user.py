def test_verify_password(user):
	assert user.verify_password("password")

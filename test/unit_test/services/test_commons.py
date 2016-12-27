from api.services.commons import *


def test_remove_blank_br():
	assert remove_blank_br("coucou<p></p>") == "coucou"
	assert remove_blank_br("coucou<p><br></p>") == "coucou"
	assert remove_blank_br("coucou<p><br></p><p></p>") == "coucou"
	assert remove_blank_br("coucou <p></p> super <p></p>") == "coucou <p></p> super "
	assert remove_blank_br("coucou<p><br></p><p><br></p><p><br></p><p></p>") == "coucou"

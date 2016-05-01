from optparse import OptionParser

from api import app


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="Use debug option")
	parser.add_option("-p", "--port", dest="port", default=5000, help="Port to broadcast")
	parser.add_option("-o", "--out", dest="out", default=False, action="store_true", help="Host to broadcast")
	options, args = parser.parse_args()

	if options.out:
		app.run('0.0.0.0', port=options.port, debug=options.debug)
	else:
		app.run(port=options.port, debug=options.debug)

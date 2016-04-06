from optparse import OptionParser

from prescrisur import app


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="Use debug option")
	options, args = parser.parse_args()

	app.run(debug=options.debug)

.PHONY: install test

install:
	(pip install -r requirements.txt && bower install)

test:
	honcho run py.test -v test

run:
	honcho start

update-spec:
	python -c 'from api.update import SpecialityUpdater; SpecialityUpdater().execute()'

update-subst:
	python -c 'from api.update import SubstanceUpdater; SubstanceUpdater().execute()'

update: update-spec update-subst

mongo-setup:
	mongo localhost:27017/Prescrisur mongo-setup.js
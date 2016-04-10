.PHONY: install test

install:
	(pip install -r requirements.txt && bower install)

test:
	py.test -v test

run:
	python runserver.py --debug

update-spec:
	python -c 'from prescrisur.update import SpecialityUpdater; SpecialityUpdater().execute()'

update-subst:
	python -c 'from prescrisur.update import SubstanceUpdater; SubstanceUpdater().execute()'

update: update-spec update-subst
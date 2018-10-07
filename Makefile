.PHONY: docs

test:
	pipenv run detox

ci:
	pipenv run pytest --cov=bsdapi -n 8

coveralls:
	pipenv run coveralls

lint:
	pipenv run tox -e lint

docs:
	-rm -rf docs/source/_rst
	-rm -rf docs/build
	pipenv run sphinx-apidoc -f bsdapi -o docs/source/_rst
	pipenv run sphinx-build -b html -c ./docs -d docs/build/doctrees . docs/build/html

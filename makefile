SHELL := /bin/bash #to be able to execute `source`

.PHONY: build
build: clean
	python setup.py  sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf dist */*.egg-info *.egg-info  build
	rm -rf .test

.PHONY: test
test: build
	test/runtest

.PHONY: upload
upload: build
	twine check dist/*
	twine upload dist/* --verbose
.PHONY: build
build: clean
	python setup.py  sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf dist */*.egg-info *.egg-info  build

.PHONY: twine
twine:
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose
	
.PHONY: upload
upload: build
	twine check dist/*
	twine upload dist/* --verbose
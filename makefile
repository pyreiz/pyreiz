
.PHONY: build
build:
	python setup.py  sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf dist */*.egg-info *.egg-info  build

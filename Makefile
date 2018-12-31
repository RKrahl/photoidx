PYTHON   = python3


build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test

sdist:
	$(PYTHON) setup.py sdist

clean:
	rm -f *~ photo/*~ photo/qt/*~ tests/*~
	rm -rf build

distclean: clean
	rm -f MANIFEST
	rm -f photo/*.pyc photo/qt/*.pyc tests/*.pyc
	rm -rf .cache
	rm -rf photo/__pycache__ photo/qt/__pycache__ tests/__pycache__
	rm -rf dist


.PHONY: build test sdist clean distclean

PYTHON   = python


build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test

sdist: doc-html
	$(PYTHON) setup.py sdist

doc-html:
	$(MAKE) -C doc html

clean:
	rm -f *~ photo/*~ photo/qt/*~ tests/*~
	rm -rf build

distclean: clean
	rm -f MANIFEST
	rm -f photo/*.pyc photo/qt/*.pyc tests/*.pyc
	rm -rf photo/__pycache__ photo/qt/__pycache__ tests/__pycache__
	rm -rf dist
	$(MAKE) -C doc distclean


.PHONY: build test sdist doc-html clean distclean

PYTHON   = python


build: 
	$(PYTHON) setup.py build

sdist: 
	$(PYTHON) setup.py sdist

clean:
	rm -f *~ photo/*~
	rm -rf build

distclean: clean
	rm -f MANIFEST
	rm -f photo/*.pyc
	rm -rf photo/__pycache__
	rm -rf dist


.PHONY: build sdist clean distclean

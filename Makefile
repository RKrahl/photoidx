PYTHON   = python


build: 
	$(PYTHON) setup.py build

sdist: 
	$(PYTHON) setup.py sdist

clean:
	rm -f *~ photo/*~ photo/qt/*~
	rm -rf build

distclean: clean
	rm -f MANIFEST
	rm -f photo/*.pyc photo/qt/*.pyc
	rm -rf photo/__pycache__ photo/qt/__pycache__
	rm -rf dist


.PHONY: build sdist clean distclean

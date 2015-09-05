PYTHON   = python


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


.PHONY: sdist clean distclean

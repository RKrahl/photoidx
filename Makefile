PYTHON   = python3
BUILDLIB = $(CURDIR)/build/lib


build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test

sdist:
	$(PYTHON) setup.py sdist

clean:
	rm -rf build
	rm -rf __pycache__

distclean: clean
	rm -f MANIFEST _meta.py
	rm -f photo-tools/__init__.py
	rm -rf dist

meta:
	$(PYTHON) setup.py meta


.PHONY: build test sdist clean distclean meta

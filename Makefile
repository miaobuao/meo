dist: $(shell find meo -type f -name "*.py") setup.py
	./setup.py sdist bdist_wheel

$(shell find meo -type f -name "*.py"):
	@touch $@

setup.py:
	@touch setup.py

upload: dist
	twine upload dist/**

install: dist
	pip install ./dist/*.whl --force-reinstall
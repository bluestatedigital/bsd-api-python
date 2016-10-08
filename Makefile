.PHONY: venv

VENV_NAME=venv

install: setup-venv requirements

clean: clean-build
	@echo "Removing compiled source..."
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f  {} +

clean-build:
	@echo "Removing build files..."
	@-rm -rf build/
	@-rm -rf dist/
	@-rm -rf *.egg-info

help:
	@echo " "
	@echo "  BSD API Library Makefile"
	@echo "  ========================"
	@echo " "
	@echo "  clean"
	@echo "    remove compiled bytecode and build source files"
	@echo "  clean-build"
	@echo "    remove only build source files"
	@echo "  install"
	@echo "    configure the virtual environment and other development dependencies"
	@echo "  lint"
	@echo "    run flake8 on the package source"
	@echo "  requirements"
	@echo "    install or update requirements in the virtual environment"
	@echo "  reset"
	@echo "    remove build and source files, and delete the virtual environment."
	@echo "    After running 'make reset', you'll need to run 'make install' again."
	@echo "  test"
	@echo "    run unit tests"
	@echo " "

install: setup-venv requirements

lint:
	-flake8 bsdapi --max-line-length=119

requirements: venv
	@touch requirements.txt
	@echo "Updating requirements..."
	. venv/bin/activate &&  \
		pip install -r requirements.txt && \
		pip install -e .

reset: clean
	@echo "Removing virtual environment..."
	@-rm -rf ./$(VENV_NAME)

setup-venv:
	virtualenv $(VENV_NAME) --no-site-packages

test:
	. venv/bin/activate && \
		pytest tests/ --cov=bsdapi

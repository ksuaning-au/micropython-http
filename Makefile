ifeq ($(OS),Windows_NT)
    RM = del /Q /F
    RRM = rmdir /Q /S
    mkdirp = mkdir $(subst /,\,$1)
    OPN = cmd /c start
else
    RM = rm -f
    RRM = rm -rf
    mkdirp = mkdir -p $1
    OPN = open
endif

.PHONY: test
test:
	python -m pytest -s --verbose

.PHONY: htmlcov
htmlcov:
	python -m pytest --cov uhttp --cov-report html
	-$(OPN) htmlcov/index.html

.PHONY: requirements
requirements:
	pip freeze > requirements.txt

.PHONY: clean
clean:
	-$(RRM) .pytest_cache
	-$(RRM) htmlcov
	-$(RM) .coverage

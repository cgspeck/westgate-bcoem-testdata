
check-types:
	poetry run mypy src

test: check-types

.PHONY: test check-types

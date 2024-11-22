ISORT = isort .
AUTOFLAKE = autoflake --remove-all-unused-imports --in-place --recursive .

# Define the targets
.PHONY: format

format:
    $(AUTOFLAKE)
    $(ISORT)
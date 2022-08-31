MAKEFLAGS += --no-print-directory

# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: Redis arXiv Search App Makefile help
# help:

SHELL:=/bin/bash
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

# help: help                      - display this makefile's help information
.PHONY: help
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'

# help:
# help: Conda Environment Setup
# help: -------------

# help: env                   - setup a Python conda env for this application
.PHONY: env
env:
	@conda create -n arXiv python=3.9 -y
	$(CONDA_ACTIVATE) arXiv
	@cd backend/ && pip install -r requirements.txt

# help:
# help:

.PHONY: usage
usage:
	@echo "Basic usage"
	@echo ""
	@echo "Targets:"
	@echo "  setup   Starts and provisions the vagrant environment"
	@echo "  tests   Execute tests"
	@echo "  clean   Destroys the vagrant environmen"
	@echo ""

.PHONY: setup
setup:
	vagrant up --provision

.PHONY: clean
clean:
	vagrant destroy -f

all-tests := $(wildcard tests/*/*Test.yml)
.NOTPARALLEL: $(all-tests)
.PHONY: $(all-tests)
$(all-tests):
	ansible-playbook $@

.PHONY: tests
tests: $(all-tests)
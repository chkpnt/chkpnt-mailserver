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
	@echo "As long as 'hostname' isn't part of the base boxes or https://github.com/hashicorp/vagrant/pull/11100"
	@echo "is merged, the VMs need to be restarted once to use the correct hostname:"
	vagrant halt
	vagrant up

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
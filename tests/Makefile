.PHONY: usage
usage:
	@echo "Basic usage"
	@echo ""
	@echo "Targets:"
	@echo "  setup   Starts and provisions the vagrant environment. Time can be saved by parallel execution (use -j)."
	@echo "  tests   Execute tests (do not use -j!)"
	@echo "  clean   Destroys the vagrant environment"
	@echo ""

vms := ns sut client mail-sink
.PHONY: setup $(vms)
setup: $(vms)
$(vms): ns
	vagrant up --provision $@

.PHONY: clean
clean:
	vagrant destroy -f

all-tests := $(wildcard tests/*/*Test.yml)
.PHONY: $(all-tests)
$(all-tests):
	ansible-playbook $@

.PHONY: tests
tests: $(all-tests)
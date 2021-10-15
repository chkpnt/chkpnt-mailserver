PROVIDER = virtualbox
GITHUB_WORKFLOW = asdf

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
	vagrant up --provision --provider=$(PROVIDER) $@

.PHONY: clean
clean:
	vagrant destroy -f

all-tests := $(wildcard tests/*/*Test.yml) $(wildcard unittests/*_tests.yml)
.PHONY: $(all-tests)
$(all-tests):
ifeq ($(TRAVIS), true)
	@echo "travis_fold:start:$@"
	$(call travis_time_start)
else ifeq ($(GITHUB_ACTIONS), true)
	@echo "::group::$@"
endif
	ansible-playbook $@
ifeq ($(TRAVIS), true)
	$(call travis_time_end)
	@echo "travis_fold:end:$@"
else ifeq ($(GITHUB_ACTIONS), true)
	@echo "::endgroup::"
endif

.PHONY: tests
tests: $(all-tests)

# Helper for Travis-CI

DATE :=
ifeq ($(shell uname -s), Darwin)
	# brew install coreutils
	DATE = gdate
else
	DATE = date
endif

define travis_time_start
	$(eval TRAVIS_TIMER_START_TIME := $$(shell $(DATE) +%s%N))
	$(eval TRAVIS_TIMER_ID := $(shell bash -c 'printf %08x $$(( RANDOM * RANDOM ))'))
	@echo "travis_time:start:$(TRAVIS_TIMER_ID)"
endef

define travis_time_end
	@ \
	START=$(TRAVIS_TIMER_START_TIME); \
	END=$$($(DATE) +%s%N); \
	DURATION=$$(( $${END} - $${START} )); \
	echo "travis_time:end:$(TRAVIS_TIMER_ID):start=$${START},finish=$${END},duration=$${DURATION}";
endef

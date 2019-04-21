*Do not use this role, it's still work in progress.*

# mailserver

The purpose of this Ansible role is to fulfill the requirements for my own mailserver.

## Requirements

*TODO ...*

## Tests
There are some tests, which use a Vagrant environment composed of four VMs:

### Virtual machines

#### `ns.test`
A custom nameserver is needed as we need other RRs than simple A-RRs. The role `nameserver` is used which configures `bind` with the zone-files needed for the test environment.

Hostname: `ns.test` <br>
FQDN: `ns.test` <br>
IP: `10.0.3.2`

#### `sut.mydomain.test`
This VM is the *system-under-test* which gets the role `chkpnt-mailserver` with all the relevant settings we want to test.

Hostname / FQDN: `sut.mydomain.test` <br>
IP: `10.0.3.10`

#### `mail-sink.theirdomain.test`
This VM uses `smtp-sink` from the package `postfix` to catch all mails and write them into `/tmp/maildump`.

Hostname / FQDN: `mail-sink.theirdomain.test` <br>
IP: `10.0.3.20`

#### `client.localdomain`
This VM is used to be the Mail User Agent (MUA).

Hostname: `client.localdomain` <br>
FQDN: `-` <br>
IP: `10.0.3.201` <br>
rDNS: `ip-10.0.3.201.someisp.test`

### Executing tests

Vagrant and VirtualBox is needed to run the tests, which are simple Ansible playbooks under [`tests/tests/*`](tests/tests/).

There is a [`Makefile`](tests/Makefile) which can be used to setup the Vagrant environment (`make setup`) and to run the tests (`make test`).
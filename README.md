*Do not use this role, it's still work in progress.*

# mailserver

The purpose of this Ansible role is to fulfill the requirements for my own mailserver.

## Requirements

*TODO ...* Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

## Role Variables

*TODO ...* A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

*TODO ...* A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

## Example Playbook

*TODO ...* Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

## Tests
There are some tests, which use a Vagrant environment composed of four VMs:

### Virtual machines

#### `ns.test`
A custom nameserver is needed as we need other RRs than simple A-RRs. The role `nameserver` is used which configures `bind` with the [zone-files](tests/testfixtures/roles/nameserver/files/var/lib/named/) needed for the test environment.

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

There is a [`Makefile`](tests/Makefile) which can be used to setup the Vagrant environment (`make setup`) and to run the tests (`make tests`).

## License

*tbd*

## Author Information

*TODO ...* An optional section for the role authors to include contact information, or a website (HTML is not allowed).
## Tests
There are some tests, which use a Vagrant environment composed of four VMs.

### Executing tests

Vagrant and VirtualBox is needed to run the tests, which are simple Ansible playbooks under [`tests/*`](tests/).

There is a [`Makefile`](Makefile) which can be used to setup the Vagrant environment (`make setup`) and to run the test suite (`make tests`).

### Test suite

| ID  | Purpose                        |
|-----|--------------------------------|
| 00* | Authentication against Postfix |
| 22* | DKIM stuff                     |
| 55* | Postfix access table           |

### Vagrant environment

#### `ns.test`
A custom nameserver is needed as we need other RRs than simple A-RRs. The role `nameserver` is used which configures `bind` with the [zone-files](testfixtures/roles/nameserver/files/var/lib/named/) needed for the test environment.

Hostname: `ns.test` <br>
FQDN: `ns.test` <br>
IP: `10.0.3.2`

#### `sut.mydomain.test`
This VM is the *system-under-test* which gets the role `chkpnt.mailserver` with all the relevant settings we want to test.

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


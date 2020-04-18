## Tests
There are some tests, which use a Vagrant environment composed of four VMs.

### Executing tests

Vagrant and VirtualBox is needed to run the tests, which are simple Ansible playbooks under [`tests/*`](tests/).

There is a [`Makefile`](Makefile) which can be used to setup the Vagrant environment (`make -j setup`) and to run the test suite (`make tests`).

### Vagrant environment

#### `ns.test`
A custom nameserver is needed as we need other RRs than simple A-RRs. The role `nameserver` is used which configures `bind` with the [zone-files](testfixtures/roles/nameserver/files/var/lib/named/) needed for the test environment.

Hostname: `ns.test` <br>
FQDN: `ns.test` <br>
IP: `10.0.3.2`

#### `sut.mydomain.test`
This VM is the *system-under-test* which gets the role `chkpnt.mailserver` with all the relevant settings we want to test.
The rspamd WebUI can be accessed via <!-- markdown-link-check-disable -->[http://10.0.3.10:11334/](http://10.0.3.10:11334/)<!-- markdown-link-check-enable--> and password [*changeme*](testfixtures/vms/sut.yml#L49-L50).

Hostname / FQDN: `sut.mydomain.test` <br>
IP: `10.0.3.10`

#### `mail-sink.theirdomain.test`
This VM uses `smtp-sink` from the package `postfix` to catch all mails and write them into `/tmp/maildump`.

Hostname / FQDN: `mail-sink.theirdomain.test` <br>
IP: `10.0.3.20`

#### `client.localdomain`
This VM is used to be the Mail User Agent (MUA).

The mismatch in hostname and rDNS is by purpose to simulate a client sending mails from 
a regular internet connection at home:
- The client is allowed to send mails if it [is authenticated](tests/outgoing/MailCanBeSentFromClientWithAuthenticationTest.yml)
- Mails sent via the local MTA is tagged as Spam if it is [received by the mailserver](tests/incoming/ReceiveMailTest.yml)

Hostname: `client.localdomain` <br>
FQDN: `-` <br>
IP: `10.0.3.201` <br>
rDNS: `ip-10.0.3.201.someisp.test`


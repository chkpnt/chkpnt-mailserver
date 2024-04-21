# Ansible role for an all-in-one mail server based on openSUSE Leap 15.5

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/chkpnt/chkpnt-mailserver/run-tests.yml?branch=main&style=flat-square&logo=github&label=Tests%20against%20latest%20openSUSE%20Leap%2015.5)](https://github.com/chkpnt/chkpnt-mailserver/actions/workflows/run-tests.yml)
[![Ansible Role](https://img.shields.io/ansible/role/d/chkpnt/mailserver?style=flat-square&logo=ansible&label=Ansible%20Galaxy%20downloads)](https://galaxy.ansible.com/chkpnt/mailserver)

The purpose of this Ansible role is to fulfill my demands on my own mail server:

- [x] Supports openSUSE Leap 15.5
- [x] Orchestration of Postfix (MTA), Dovecot (MDA) and Rspamd
- [x] Postfix uses Dovecot for authentication (SMTP AUTH through Dovecot SASL)
- [x] No databases for configuration, just plain files
- [x] Mails to specific addresses can be relayed to another MTA
- [x] Mails to specific addresses can be rejected
- [x] Outgoing mails are DKIM signed
- [x] Relayed mails are ARC signed
- [x] Catch-all accounts can be configured
- [x] Multiple domains are supported
- [x] Sieve rules can be used
- Spam
  - [x] Spam with a high score is rejected
  - [x] Spam detection can be disabled for specific senders (addresses or domains)
  - [x] Potential spam is not automatically delivered into a Spam folder (of course a customa Sieve rule can be used)
  - [x] Potential spam is greylisted
  - [x] Spam can be learnt by moving the mail into a special IMAP folder
  - [x] Spam can be learnt by applying the Junk flag, which is used by Thunderbird
  - [x] Ham can be learnt by moving the mail into a special IMAP folder
  - [x] Ham can be learnt by applying the NonJunk flag, which is used by Thunderbird
  - [x] Ham can be learnt by marking the mail with a green flag in the iOS Mail App
- Antivirus
  - [x] Integration of [ClamAV](https://www.clamav.net/)
  - [x] Integration of [Fangfrisch](https://rseichter.github.io/fangfrisch/)
  - [ ] Integration of VirusTotal.com
  - [x] Infected mails are rejected
- [x] Nice reports (rspamd WebUI is sufficient for me)
- [x] Nearly all requirements are covered by tests
- [x] Tests are executed by a CI system

## Usage and configuration

This role is available via Ansible Galaxy under the name `chkpnt.mailserver`. It can be installed with
```
$ ansible-galaxy install chkpnt.mailserver
```
and used within a playbook like
```yaml
---
- hosts: server1
  remote_user: root
  roles:
  - role: chkpnt.mailserver
    vars:
      mail_domain: example.com
      mail_hostname: server1.example.com
      mail_mailname: server1.example.com
      mail_mailbox_domains:
        - example.com
        - example.net
        - example.org
      mail_ssl:
        certificate: '/etc/ssl/servercerts/example.com.crt.pem'
        private_key: '/etc/ssl/private/example.com.privkey.pem'
        generate_certificate_for_test: yes
        generate_safe_primes_for_dh: yes # https://www.openssl.org/news/secadv/20160128.txt
      mail_dkim_keys:
        - { domain: example.com, selector: 'key1', private_key: '/var/lib/rspamd/dkim/example.com.key1.key' }
        - { domain: example.org, selector: 'key1', private_key: '/var/lib/rspamd/dkim/example.org.key1.key' }
        - { domain: example.net, selector: 'key1', private_key: '/var/lib/rspamd/dkim/example.net.key1.key' }
      # Hash can be computated with doveadm.
      # I recommend using Blowfish as the hashing schema, the ideal number of rounds depends on your system.
      # > doveadm pw -s BLF-CRYPT -r 10
      mail_accounts:
        - { user: 'john.doe@example.com', password: '{BLF-CRYPT}$2y$10$6W9VYuRklwLg8y2UoP6YHuK5Q8g7g.LOJdSa7K4CgoVMmARNYMVMK' } # Password: changeme
        - { user: 'jane.doe@example.com', password: '{BLF-CRYPT}$2y$10$wZtIn5uHAsbsMgMmOdBdU.qbRgrQxfeej65G63aUxMaDNEHfb8P2e' } # Password: changeme
      mail_mailboxes:
        - { name: 'john.doe@example.com', path: '/srv/mail/john' }
        - { name: 'jane.doe@example.com', path: '/srv/mail/jane' }
      mail_aliases:
        # a self-referencing alias is needed if the mail_transports is used
        - { for: 'gmail@example.com', destination: 'gmail@example.com' }
        # normal aliases
        - { for: 'wedding@example.com', destination: 'family@example.com' }
        - for: 'family@example.com'
          destination:
            - 'john.doe@example.com'
            - 'jane.doe@example.com'
        # Catch-Alls:
        - { for: '@example.com', destination: 'john.doe@example.com' }
        - { for: '@example.org', destination: 'john.doe@example.com' }
        - { for: '@example.net', destination: 'john.doe@example.com' }
      mail_recipient_restrictions:
        - for: 'reject@example.com'
          action: 'REJECT This address is not supposed to receive mails!'
      mail_transports:
        - for: 'gmail@example.com'
          nexthop: 'smtp:gmail.com'
      mail_spam:
        greylisting_delay: 5min
        thresholds: # Requirement: greylist < add_header < reject
          greylist: 4
          add_header: 6
          reject: 15
        controller:
          # Controller worker is used to manage rspamd stats, to learn rspamd and to serve WebUI.
          # https://rspamd.com/doc/workers/controller.html
          # If you access the WebUI from localhost, you won't be asked for the password as localhost is a "secure_ip"
          # > rspamadm pw
          password: '$2$c75qgo1b8brudgq7wokg8wxr5qiby84p$ye6ss3ymc4h4u4swk3fhx3ph7jesahqrzw8kkxwhyfb14g4rkfhb' # Password: changeme
          bind_socket: 'localhost:11334' 
        # Regexps are supported
        allowlist_domain:
          - foobar.test
        allowlist_email:
          - /.*@important.test/
```

The defaults of the variables are defined in [defaults/main.yml](defaults/main.yml). All variables refering to `example.com` or similar are expected to be explicitly declared in your playbook.

The playbook [tests/testfixtures/vms/sut.yml](tests/testfixtures/vms/sut.yml) used by the tests is a good example, too.

## Development

I recommend to set up a Python environment using [*pipenv*](https://github.com/pypa/pipenv). On macOS, *pipenv* can be installed using Homebrew:

```
$ brew install pipenv
```

To use the Python environment with pipenv, just enter the following commands:

```
$ pipenv install --dev
$ pipenv shell
```

In order to run the tests, VirtualBox and Vagrant are required. On macOS, these dependencies can be installed using Homebrew as well:

```
$ brew install --cask virtualbox
$ brew install --cask vagrant
```

For managing your Vagrant virtual machines, I can recommend the use of [Vagrant-Manager](http://vagrantmanager.com/), a small utility app for the menu bar.

```
$ brew install --cask vagrant-manager
```

Additional information about the tests can be found in the corresponding [document](tests/README.md).

## License

Apache-2.0 

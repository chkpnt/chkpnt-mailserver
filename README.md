*Do not use this role, it's still work in progress.*

# mailserver

[![Build Status](https://img.shields.io/travis/com/chkpnt/chkpnt-mailserver/master?label=Tests&style=flat-square)](https://travis-ci.com/chkpnt/chkpnt-mailserver)

The purpose of this Ansible role is to fulfill my demands on my own mailserver:

- [x] Supports openSUSE Leap 15.1
- [x] Orchestration of Postfix (MTA), Dovecot (MDA) and Rspamd
- [x] Postfix uses Dovecot for authentication (SMTP AUTH through Dovecot SASL)
- [x] No databases, just plain files
- [x] Outgoing mails are DKIM signed
- [x] Mails to specific addresses can be relayed to another MTA
- [x] Mails to specific addresses can be rejected
- [x] Catch-all accounts can be configured
- [x] Multiple domains are supported
- [x] Sieve rules can be used
- Spam
  - [x] Spam with a high score is rejected
  - [x] Potential Spam is not automatically delivered into a Spam folder (of course a customa Sieve rule can be used)
  - [x] Potiantial spam is greylisted
  - [x] Spam can be learnt by moving the mail into a special IMAP folder
  - [ ] Spam can be learnt by applying the Junk flag, which is used by Thunderbird
  - [x] Ham can be learnt by moving the mail into a special IMAP folder
  - [x] Ham can be learnt by applying the NonJunk flag, which is used by Thunderbird
  - [x] Ham can be learnt by marking the mail with a green flag in the iOS Mail App
- Antivirus
  - [x] Integration of ClamAV
  - [ ] Integration of VirusTotal.com
  - [x] Infected mails are rejected
- [x] Nice reports (rspamd WebUI is sufficient for me)
- [x] Nearly all requirements are covered by tessts
- [x] Tests are executed by a CI system

## Requirements

*TODO ...* Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

## Role Variables

*TODO ...* A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

## Dependencies

*TODO ...* A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

## Example Playbook

Please have a look at [tests/testfixtures/vms/sut.yml](tests/testfixtures/vms/sut.yml) and [tests/manual/playbook.yml](tests/manual/playbook.yml).

## License

Apache-2.0 

## Author Information

*TODO ...* An optional section for the role authors to include contact information, or a website (HTML is not allowed).
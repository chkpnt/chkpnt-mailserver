# Ansible managed

# Just a little Sieve script for try-out-purposes
require ["vnd.dovecot.debug", "environment", "imapsieve"];
if environment :matches "imap.mailbox" "*" {
    set "mailbox" "${1}";
}
debug_log "imap.mailbox = ${mailbox}";

# Ansible managed

# https://github.com/dovecot/pigeonhole/blob/master/doc/rfc/spec-bosch-sieve-extprograms.txt

require ["vnd.dovecot.debug", "vnd.dovecot.pipe", "copy"];

debug_log "Passing mail to rspamd for learning as Ham";
pipe :copy "rspamc" ["learn_ham"];

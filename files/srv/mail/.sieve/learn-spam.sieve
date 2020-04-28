# Ansible managed

# https://github.com/dovecot/pigeonhole/blob/master/doc/rfc/spec-bosch-sieve-extprograms.txt
require ["vnd.dovecot.pipe", "copy"];
pipe :copy "rspamc" ["learn_spam"];
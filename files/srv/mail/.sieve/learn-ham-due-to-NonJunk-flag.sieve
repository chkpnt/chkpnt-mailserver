# Ansible managed

require ["vnd.dovecot.debug", "imap4flags", "vnd.dovecot.pipe", "copy"];

# see https://github.com/chkpnt/chkpnt-mailserver/issues/5
if allof (hasflag :contains "$MailFlagBit0",
          hasflag :contains "$MailFlagBit1") {
    debug_log "Replacing green flag (iOS Mail) with NonJunk flag";
    removeflag ["$MailFlagBit1", "$MailFlagBit0"];
    addflag "NonJunk";
}

if hasflag :contains "NonJunk" {
    debug_log "Passing mail to rspamd for learning as Ham";
    pipe :copy "rspamc" ["learn_ham"];
}
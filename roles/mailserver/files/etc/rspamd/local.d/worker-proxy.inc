# Ansible managed

upstream "local" {
  self_scan = yes;
}

bind_socket = "/run/rspamd/worker-proxy.socket mode=0660";

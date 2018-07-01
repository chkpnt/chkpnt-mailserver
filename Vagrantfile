# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

    hostname = "leap15"

    # Box
    #config.vm.box = "bento/opensuse-leap-42.3"
    #config.vm.box = "opensuse/openSUSE-42.3-x86_64"
    config.vm.box = "opensuse/openSUSE-15.0-x86_64"

    config.vm.provision :ansible do |ansible|
        ansible.force_remote_user = true
        ansible.compatibility_mode = "2.0"
        ansible.verbose = true
        ansible.playbook = "playbook.yml"
    end

    config.vm.network :forwarded_port, host: 10025, guest: 25
    config.vm.network :forwarded_port, host: 10993, guest: 993
    config.vm.network :forwarded_port, host: 11334, guest: 11334

    # Setup
    # config.vm.provision :shell, :inline => "touch .hushlogin"
    # config.vm.provision :shell, :inline => "hostnamectl set-hostname #{hostname} && locale-gen #{locale}"
    # config.vm.provision :shell, :inline => "apt-get update --fix-missing"
    # config.vm.provision :shell, :inline => "apt-get install -q -y g++ make git curl vim"

    # Lang
    # config.vm.provision :shell, :inline => "apt-get install -q -y mono-complete"

end
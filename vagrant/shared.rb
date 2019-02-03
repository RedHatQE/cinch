ENV['VAGRANT_NO_PARALLEL'] = 'yes'
$ip = 2

def get_username(base_box)
    if base_box.start_with?('centos')
        return 'centos'
    elsif base_box == 'generic/rhel8'
        return 'cloud-user'
    elsif base_box.include?('rhel')
        return 'root'
    else
        return 'fedora'
    end
end

def get_image(base_box)
    if base_box == 'centos/7'
        return 'CentOS-7-x86_64-GenericCloud-released-latest'
    elsif base_box == 'centos/6'
        return 'CentOS-6-x86_64-GenericCloud-1612'
    elsif base_box == 'fedora/26-cloud-base'
        return 'Fedora-Cloud-Base-26-compose-latest'
    elsif base_box == 'generic/rhel7'
		return 'rhel-7.6-server-x86_64-updated'
    elsif base_box == 'generic/rhel8'
        return 'rhel-8.0-x86_64-latest'
    elsif base_box == 'rhel6'
        return 'rhel-6.9-server-x86_64-updated'
    end
end

def local_setup(node, base_box)
    node.vm.box = base_box
    node.vm.network "private_network", ip: "192.168.8.#{$ip}", netmask: "255.255.255.0"
    $ip += 1
end

def vm(config, name, base_box="centos/7")
    config.vm.define name do |nodeconfig|
        nodeconfig.vm.hostname = name + ".box"
        # Provider-specific setup
        nodeconfig.vm.provider :libvirt do |lv, override|
            local_setup(override, base_box)
        end
        nodeconfig.vm.provider :virtualbox do |vb, override|
            local_setup(override, base_box)
        end
        nodeconfig.vm.provider :openstack do |os, override|
            os.image = get_image(base_box)
            os.server_name = ENV['USER'] + '-' + name
            override.ssh.username = get_username(base_box)
            override.ssh.pty = true
        end
        # Setup Ansible configuration, if we're asked
        nodeconfig.vm.provision :shell, inline: "sed -E -i /etc/sudoers -e '/Defaults\\s+requiretty/d'"
        if base_box.start_with?('fedora')
            nodeconfig.vm.provision "shell", inline: "sudo dnf install -y python"
        end
        if block_given?
            nodeconfig.vm.provision "ansible" do |ansible|
                    ansible.playbook = "../../cinch/site.yml"
                    ansible.limit = "all"
                    ansible.verbose = "-v"
                    yield ansible
            end
        end
        # Disable shared folder, since we want to simulate the real world
        nodeconfig.vm.synced_folder "../..", "/vagrant", disabled: true
        if Vagrant.has_plugin?('vagrant-cachier')
            # Needs to be :machine, because in multi-vm environments, when they both hit a
            # download point, then things can get hairy when both boxes try to lock
            config.cache.scope = :machine
            config.cache.synced_folder_opts = {
                type: :sshfs
            }
        end
    end
end

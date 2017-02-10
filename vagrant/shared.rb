$ip = 2

def vm(config, name, base_box="centos/7")
    config.vm.define name do |nodeconfig|
        nodeconfig.vm.box = base_box
        nodeconfig.vm.hostname = name + ".box"
        nodeconfig.vm.network "private_network", ip: "192.168.8.#{$ip}", netmask: "255.255.255.0"
        $ip += 1
        if block_given?
            nodeconfig.vm.provision "ansible" do |ansible|
                    ansible.playbook = "../../cinch/site.yml"
                    ansible.limit = "all"
                    ansible.verbose = "-v"
                    yield ansible
            end
        end
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

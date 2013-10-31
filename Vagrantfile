# -*- mode: ruby -*-
# vim: set ft=ruby sw=2 :

Vagrant.configure("2") do |config|
  config.omnibus.chef_version = "11.4.0"

  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.provider :aws do |aws, override|
    override.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"
    aws.access_key_id = ENV['AWS_ACCESS_KEY_ID']
    aws.secret_access_key = ENV['AWS_SECRET_ACCESS_KEY']
    aws.keypair_name = "YOUR AWS KEYPAIR NAME"
    aws.ami = "ami-a73264ce"
    aws.instance_type = "m1.large"
    aws.region = "us-east-1"
    aws.security_groups = ["open"]
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = "THE LOCAL PATH TO YOUR AWS PRIVATE KEY"
  end

  config.vm.provider :digital_ocean do |provider, override|
    override.ssh.private_key_path = '~/.ssh/id_rsa'
    override.vm.box = 'digital_ocean'
    override.vm.box_url = "https://github.com/smdahlen/vagrant-digitalocean/raw/master/box/digital_ocean.box"
    provider.client_id = 'YOUR CLIENT ID'
    provider.api_key = 'YOUR API KEY'
  end

  config.vm.provider :virtualbox do |v, override|
    override.vm.box_url = "http://files.vagrantup.com/precise64.box"
    v.customize ["modifyvm", :id, "--memory", 2 * 1024]
    v.customize ["modifyvm", :id, "--cpus", "2"]
  end

  config.berkshelf.enabled = true

  config.vm.provision :chef_solo do |chef|

    chef.add_recipe 'sudo'
    chef.add_recipe 'apt::default'
    chef.add_recipe 'git'
    chef.add_recipe 'nginx'
    chef.add_recipe 'postgresql::server'
    chef.add_recipe 'django'
    chef.add_recipe 'django::nginx'
    chef.add_recipe 'django::postgresql'
    chef.add_recipe 'django::server'
  end
end

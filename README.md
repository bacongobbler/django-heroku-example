Up and Running with Django in the cloud
=======================================

this application shows standard practices with getting set up
and hit the ground running with Django on EC2 or other cloud
providers such as Heroku.

a note: this guide assumes Ubuntu 12.04.3 LTS as the host OS.

# deploy to ec2

first, sign up for an EC2 account and [grab your access key and secret key](https://portal.aws.amazon.com/gp/aws/securityCredentials). Then, open up `~/.bashrc` and enter the following:

    export AWS_ACCESS_KEY_ID="YOUR ACCESS KEY"
    export AWS_SECRET_ACCESS_KEY="YOUR SECRET KEY"

install the ec2 api tools:

    sudo apt-get install -qy ec2-api-tools

if you run `ec2-describe-regions` and get no errors, then you're set this up properly.

next, install ruby and the ec2 plugin for knife, as well as a chef solo plugin for knife. these plugins will help assist us with application deployment to EC2.

    sudo apt-get install ruby-1.9.3 && sudo gem install knife-ec2 knife-solo

## configure knife ec2 and knife solo

To configure knife ec2, edit the file `~/.chef/knife.rb` and append the following lines

    knife[:aws_access_key_id]       = "#{ENV['AWS_ACCESS_KEY_ID']}"
    knife[:aws_secret_access_key]   = "#{ENV['AWS_SECRET_ACCESS_KEY']}"

With this, the command `knife ec2 server list` should provide reasonable output.

## from vagrant to ec2

Ok, know we're ready to go. Let's use knife to create a new EC2 instance. In the following, I'm using ami-a73264ce, a 64-bit Ubuntu 12.04.3 AMI for the AWS us-east-1 region. Check the list of published Ubuntu AMIs to make your own choice.

    knife ec2 server create --ssh-key <mykey> --ssh-user ubuntu --node-name django --groups default -I ami-a73264ce -G default --flavor=m1.large

mykey should be a EC2 key pair in the chosen AWS region, that you have created using the EC2 API Tools or the AWS Console.

Now, since we're already managing our project's cookbooks with Berkshelf, we can leverage Berkshelf to populate the knife solo kitchen cookbook directory

    cd django-heroku-example
    berks install

We're almost done, we just need to prepare the new instance…

    cd django-heroku-example
    knife solo prepare ubuntu@ec2-xx-xx-xx-xx.eu-west-1.compute.amazonaws.com

    Bootstrapping Chef...
    . . .  
    Generating node config 'nodes/ec2-xx-xx-xx-xx.eu-west-1.compute.amazonaws.com.json'...

…and create an appropriate run list for Django

    vim nodes/ec2-xx-xx-xx-xx.eu-west-1.compute.amazonaws.com.json
    { "run_list": ["recipe[django]"] }

And with that, we can upload the knife solo kitchen including the cookbooks to the EC2 instance, and run chef-solo there

    knife solo cook ubuntu@ec2-xx-xx-xx-xx.eu-west-1.compute.amazonaws.com

There. Almost as good as vagrant provision, but on an Amazon EC2 instance!

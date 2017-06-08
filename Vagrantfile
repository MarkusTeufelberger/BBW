Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.synced_folder ".", "/vagrant_data"

  config.vm.provision "shell", inline: <<-SHELL
    echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
    curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
    apt-get update
    apt-get upgrade -y
    apt-get install -y bazel automake libtool pkg-config python2.7
    bazel version
  SHELL
end

<<!
 **********************************************************
 * Author        : clp
 * Email         : 328566090@qq.com
 * Last modified : 2019-09-07 15:23
 * Filename      : install_docker.sh
 * Description   : install docker 
 * *******************************************************
!
# first remove old docker version
sudo apt-get remove docker docker-engine docker-ce docker-ce-cli docker.io

# update the apt package index
sudo apt-get update

# download script and install
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh --mirror Aliyun

# start
sudo systemctl enable docker
sudo systemctl start docker

# on Ubuntu 14.04
# sudo service docker start

# create docker group
# sudo groupadd docker

# add user to the docker group
# sudo usermod -aG docker $USER

# run the test
# docker run hello-world
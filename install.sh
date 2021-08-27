sudo apt install awscli
sudo apt install docker.io
sudo apt install unzip
sudo apt install npm
sudo usermod -aG docker $USER
newgrp docker
curl -L https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip -o aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
which sam
sam --version
npm install -g artillery@latest
artillery dino
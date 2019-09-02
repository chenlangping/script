# Author : clp
# install zsh
# Githup : https://github.com/robbyrussell/oh-my-zsh
sudo apt install -y zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# add plugins
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
sed -i 's/^plugins=(/plugins=(\n  zsh-autosuggestions\n  zsh-syntax-highlighting\n  /' ~/.zshrc

# login into oh-my-zsh and run:
# source ~/.zshrc
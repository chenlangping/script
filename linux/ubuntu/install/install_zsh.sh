<<!
 **********************************************************
 * Author        : clp
 * Email         : 328566090@qq.com
 * Last modified : 2019-09-02 10:38
 * Filename      : install_zsh.sh
 * Description   : install zsh  
 * *******************************************************
!
# Githup : https://github.com/robbyrussell/oh-my-zsh
sudo apt install -y zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# change theme
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="bira"/' ~/.zshrc

# add plugins
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
sed -i 's/^plugins=(/plugins=(\n  zsh-autosuggestions\n  zsh-syntax-highlighting\n  z\n  /' ~/.zshrc

# login into oh-my-zsh and run:
# source ~/.zshrc

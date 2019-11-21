<<!
 **********************************************************
 * Author        : clp
 * Email         : 328566090@qq.com
 * Last modified : 2019-11-21 10:13
 * Filename      : install_linuxbrew.sh
 * Description   : 
 * *******************************************************
!
#!/bin/sh
sudo apt-get install build-essential curl file git
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
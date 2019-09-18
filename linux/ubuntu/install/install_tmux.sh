#!/bin/sh
<<!
 **********************************************************
 * Author        : clp
 * Email         : 328566090@qq.com
 * Last modified : 2019-09-04 15:29
 * Filename      : install_tmux.sh
 * Description   : install tmux and make some config
 * *******************************************************
!
sudo apt-get install tmux
cd
git clone https://github.com/gpakosz/.tmux.git
ln -s -f .tmux/.tmux.conf
cp .tmux/.tmux.conf.local .
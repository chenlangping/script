<<!
 **********************************************************
 * Author        : clp
 * Email         : 328566090@qq.com
 * Last modified : 2019-09-11 19:46
 * Filename      : install_lnmp.sh
 * Description   : install nginx php and MySQL 
 * See more      : https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-in-ubuntu-16-04
 * *******************************************************
!
#!/bin/bash

# update first
sudo apt-get update

# install web server
sudo apt-get install nginx

# install MySQL
sudo apt-get install mysql-server

# install PHP
sudo apt-get install php-fpm php-mysql

# config PHP for secure
# vim /etc/php/7.0/fpm/php.ini
# cgi.fix_pathinfo=0
# sudo systemctl restart php7.0-fpm

# config nginx to use php_fpm
# sudo vim /etc/nginx/sites-available/default
# uncomment the comment about php

# check the configuration and restart the service
# sudo nginx -t
# sudo systemctl reload nginx

<<!
 **********************************************************
 * Author        : clp
 * Email         : 328566090@qq.com
 * Last modified : 2019-10-23 15:36
 * Filename      : uninstall_postgresql.sh
 * Description   : 
 * *******************************************************
!
apt-get --purge remove postgresql\* 
rm -r /etc/postgresql/ 
rm -r /etc/postgresql-common/ 
rm -r /var/lib/postgresql/ 
userdel -r postgres 
groupdel postgres

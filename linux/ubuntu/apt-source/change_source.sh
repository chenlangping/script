<<!
 **********************************************************
 * Author        : clp
 * Email         : 328566090@qq.com
 * Last modified : 2019-09-02 10:47
 * Filename      : change_source.sh
 * Description   : automaticly change apt source to aliyun
 * *******************************************************
!
#!/bin/bash

# first back up
mv /etc/apt/sources.list /etc/apt/sources.list.bak

realease_version=$( (lsb_release -a) | awk '{print $2}' | tail -n 1 )
echo "\
deb http://mirrors.aliyun.com/ubuntu/ $realease_version main multiverse restricted universe
deb http://mirrors.aliyun.com/ubuntu/ $realease_version-backports main multiverse restricted universe
deb http://mirrors.aliyun.com/ubuntu/ $realease_version-proposed main multiverse restricted universe
deb http://mirrors.aliyun.com/ubuntu/ $realease_version-security main multiverse restricted universe
deb http://mirrors.aliyun.com/ubuntu/ $realease_version-updates main multiverse restricted universe
deb-src http://mirrors.aliyun.com/ubuntu/ $realease_version main multiverse restricted universe
deb-src http://mirrors.aliyun.com/ubuntu/ $realease_version-backports main multiverse restricted universe
deb-src http://mirrors.aliyun.com/ubuntu/ $realease_version-proposed main multiverse restricted universe
deb-src http://mirrors.aliyun.com/ubuntu/ $realease_version-security main multiverse restricted universe
deb-src http://mirrors.aliyun.com/ubuntu/ $realease_version-updates main multiverse restricted universe " > /etc/apt/sources.list
sudo apt-get update

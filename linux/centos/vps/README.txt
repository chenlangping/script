# before install bbr
yum update -y 
yum upgrade -y

# after installing shadowsocks server
vim /etc/shadowsocks/config.json 

# and change server to let it listen both ipv4 and ipv6
"server":["[::0]", "0.0.0.0"],

# at last, restart shadowsocks
service shadowsocks restart

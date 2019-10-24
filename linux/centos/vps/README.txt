# before install bbr
yum update -y 
yum upgrade -y

# after installing shadowsocks server
vim /etc/shadowsocks.json 

# and change server to let it listen ipv6
"server":"::",

# at last, restart shadowsocks
service shadowsocks restart

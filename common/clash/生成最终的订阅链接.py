import urllib.parse

ip = "服务器"
port = "25500"
target = "clash"

subscription_link = [
    "订阅链接1",
    "订阅链接2"
]

my_clash_config = "https://raw.githubusercontent.com/chenlangping/script/refs/heads/master/common/clash/clash_remote_config.ini"
my_clash_config_after_url_encode = urllib.parse.quote(my_clash_config, safe='')

# 将subscription_link中间用|分割  接着用URLEncode
sub_url = "|".join(subscription_link)
sub_url_after_url_encode = urllib.parse.quote(sub_url, safe='')

print(f"http://{ip}:{port}/sub?target={target}&url={sub_url_after_url_encode}&config={my_clash_config_after_url_encode}")
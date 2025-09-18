import base64

# ====================================================================
# --- 请在这里填入你的服务器配置 ---
#
# 只需要修改这个区域内的信息即可
# ====================================================================

# 你的服务器公网 IP 地址 (必须填写)
SERVER_IP = "123.45.67.89" 

# Docker 命令中 -p 参数指定的端口
SERVER_PORT = "8888"

# Docker 命令中 -e PASSWORD 参数设置的密码
PASSWORD = "Sp2fYt"

# Docker 命令中 -e METHOD 参数设置的加密方法
METHOD = "aes-256-cfb"

# Docker 命令中 -e PROTOCOL 参数设置的协议
PROTOCOL = "auth_sha1_v4"

# Docker 命令中 -e OBFUSCATE 参数设置的混淆
OBFUSCATE = "tls1.2_ticket_auth"

# [可选] 为这个链接添加一个备注，方便在客户端中识别
REMARKS = "我的阿里云服务器"

# ====================================================================
# --- 脚本核心逻辑，无需修改 ---
# ====================================================================

def urlsafe_b64_encode(data_str: str) -> str:
    """对字符串进行 URL安全的 Base64 编码，并移除末尾的'='"""
    encoded_bytes = base64.urlsafe_b64encode(data_str.encode('utf-8'))
    return encoded_bytes.decode('utf-8').rstrip('=')

def generate_ssr_link():
    """生成 SSR 链接"""
    
    # 1. 对密码、备注和分组进行 Base64 编码
    encoded_password = urlsafe_b64_encode(PASSWORD)
    encoded_remarks = urlsafe_b64_encode(REMARKS)
    
    # 2. 拼接主要的配置部分
    # 格式: ip:port:protocol:method:obfs:password_b64
    main_part = f"{SERVER_IP}:{SERVER_PORT}:{PROTOCOL}:{METHOD}:{OBFUSCATE}:{encoded_password}"
    
    # 3. 拼接参数部分
    # 格式: /?obfsparam=...&protoparam=...&remarks=...&group=...
    # obfsparam 和 protoparam 你的命令里没有，所以留空
    params_part = f"/?obfsparam=&protoparam=&remarks={encoded_remarks}&group="
    
    # 4. 将主配置和参数部分组合成一个完整的待编码字符串
    full_unencoded_string = main_part + params_part
    
    print("--- 步骤分解 ---")
    print(f"原始密码: {PASSWORD} -> Base64编码后: {encoded_password}")
    print(f"待编码的完整字符串: {full_unencoded_string}\n")
    
    # 5. 对整个字符串进行 Base64 编码
    final_encoded_part = urlsafe_b64_encode(full_unencoded_string)
    
    # 6. 在最前面加上协议头 "ssr://"
    ssr_link = "ssr://" + final_encoded_part
    
    return ssr_link

# --- 主程序入口 ---
if __name__ == "__main__":
    if SERVER_IP == "123.45.67.89" or not SERVER_IP:
        print("!!! 警告: 请务必在脚本顶部将 SERVER_IP 修改为你自己的服务器公网IP地址！\n")
        exit(1)
    
    final_link = generate_ssr_link()
    
    print("--- 生成结果 ---")
    print("你的 SSR 链接已生成：")
    print(final_link)
    print("\n")
    print(urlsafe_b64_encode(final_link))

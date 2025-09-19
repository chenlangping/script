#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import base64
import sys
import subprocess # 导入 subprocess 模块

# --- 配置 ---
CONFIG_FILE_PATH = "/etc/shadowsocks-r/config.json"
SERVER_NAME = "阿里云服务器"

def get_public_ip():
    """
    通过执行 'curl ip.sb' 命令获取本机的公网 IP 地址。
    """
    try:
        # 定义要执行的命令
        command = ["curl", "ip.sb"]
        print "[*] 正在执行命令: " + " ".join(command)
        
        # 执行命令并捕获输出
        # .strip() 用于移除 curl 输出末尾可能存在的换行符
        ip = subprocess.check_output(command).strip()
        
        print "[*] 成功获取到公网 IP: " + ip
        return ip
    except subprocess.CalledProcessError as e:
        print >> sys.stderr, "[!] 错误：'curl ip.sb' 命令执行失败，无法连接。"
        print >> sys.stderr, "    返回码: " + str(e.returncode)
        return None
    except OSError as e:
        print >> sys.stderr, "[!] 错误：'curl' 命令未找到。"
        print >> sys.stderr, "    请确认您的服务器已安装 curl (apt install curl / yum install curl)。"
        print >> sys.stderr, "    具体错误: " + str(e)
        return None
    except Exception as e:
        print >> sys.stderr, "[!] 获取 IP 时发生未知错误。"
        print >> sys.stderr, "    具体错误: " + str(e)
        return None


def generate_ssr_link(config, server_name):
    """
    根据给定的 SSR JSON 配置字典生成 ssr:// 订阅链接。
    """
    try:
        # 从配置中提取必要参数
        server = config.get("server", "")
        server_port = config.get("server_port", 8888)
        protocol = config.get("protocol", "origin")
        method = config.get("method", "aes-256-cfb")
        obfs = config.get("obfs", "plain")
        password = config.get("password", "")
        obfs_param = config.get("obfs_param", "")
        protocol_param = config.get("protocol_param", "")

        # 对密码进行 URL-safe Base64 编码 (移除末尾的 '=')
        password_b64 = base64.urlsafe_b64encode(password.encode('utf-8')).rstrip('=')

        # 构建主要部分
        main_part = "%s:%s:%s:%s:%s:%s" % (server, server_port, protocol, method, obfs, password_b64)

        # 构建参数部分
        params = {}
        if obfs_param:
            obfsparam_b64 = base64.urlsafe_b64encode(obfs_param.encode('utf-8')).rstrip('=')
            params['obfsparam'] = obfsparam_b64
        if protocol_param:
            protoparam_b64 = base64.urlsafe_b64encode(protocol_param.encode('utf-8')).rstrip('=')
            params['protoparam'] = protoparam_b64
        if server_name:
            remark_b64 = base64.urlsafe_b64encode(server_name.encode('utf-8')).rstrip('=')
            params['remarks'] = remark_b64

        # 将参数字典转换为查询字符串
        params_str = '&'.join(["%s=%s" % (key, value) for key, value in params.items()])

        # 组合成完整的待编码字符串
        if params_str:
            full_str = "%s/?%s" % (main_part, params_str)
        else:
            full_str = main_part

        # 对整个字符串进行 URL-safe Base64 编码
        encoded_full_str = base64.urlsafe_b64encode(full_str.encode('utf-8')).rstrip('=')

        # 返回最终的 ssr:// 链接
        return "ssr://" + encoded_full_str

    except Exception as e:
        print >> sys.stderr, "[!] 生成链接时出错: " + str(e)
        return None

def encode_subscription(ssr_link):
    """
    将 SSR 链接进行 base64 编码，用于订阅
    """
    try:
        # 对 SSR 链接进行标准 base64 编码
        encoded_subscription = base64.b64encode(ssr_link.encode('utf-8'))
        return encoded_subscription
    except Exception as e:
        print >> sys.stderr, "[!] 编码订阅链接时出错: " + str(e)
        return None

def main():
    """
    主执行函数
    """
    # 1. 获取公网 IP
    public_ip = get_public_ip()
    if not public_ip:
        sys.exit(1)

    # 2. 读取并解析 JSON 配置文件
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            ssr_config = json.load(f)
        print "[*] 成功读取配置文件: " + CONFIG_FILE_PATH
    except IOError:
        print >> sys.stderr, "[!] 错误: 找不到或无权限读取配置文件 '" + CONFIG_FILE_PATH + "'。"
        print >> sys.stderr, "    请确认文件存在且权限正确，或尝试使用 'sudo' 运行此脚本。"
        sys.exit(1)
    except ValueError:
        print >> sys.stderr, "[!] 错误: 配置文件 '" + CONFIG_FILE_PATH + "' 格式不正确。"
        sys.exit(1)

    # 3. 将配置中的 server 地址替换为公网 IP
    ssr_config["server"] = public_ip
    print "[*] 已将服务器地址更新为: " + public_ip
    print "[*] 服务器名称设置为: " + SERVER_NAME

    # 4. 生成 SSR 链接
    ssr_link = generate_ssr_link(ssr_config, SERVER_NAME)

    # 5. 打印最终结果
    if ssr_link:
        print "\n" + "="*50
        print "🎉 成功生成 SSR 订阅链接! 🎉"
        print "="*50
        print "原始 SSR 链接:"
        print ssr_link
        print "\n" + "-"*50
        
        # 6. 新增：生成 base64 编码的订阅链接
        encoded_subscription = encode_subscription(ssr_link)
        if encoded_subscription:
            print "Base64 编码的订阅链接:"
            print encoded_subscription
            print "-"*50
            print "💡 提示: 将上面的 Base64 编码链接复制到 SSR 客户端的订阅地址中使用"
        
        print "="*50

if __name__ == "__main__":
    main()
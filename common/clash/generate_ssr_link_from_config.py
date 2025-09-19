#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import base64
import sys
import subprocess

# --- 配置 ---
CONFIG_FILE_PATH = "/etc/shadowsocks-r/config.json"


def get_public_ip():
    """
    通过执行 'curl ip.sb' 命令获取本机的公网 IP 地址。
    """
    try:
        command = ["curl", "ip.sb"]
        print("[*] 正在执行命令: " + " ".join(command))

        ip = subprocess.check_output(command)
        # 兼容 Python2/3: 确保 ip 为 str
        if isinstance(ip, bytes):
            ip = ip.decode("utf-8", "ignore")
        ip = ip.strip()

        print("[*] 成功获取到公网 IP: " + ip)
        return ip
    except subprocess.CalledProcessError as e:
        print("[!] 错误：'curl ip.sb' 命令执行失败，无法连接。", file=sys.stderr)
        print("    返回码: " + str(e.returncode), file=sys.stderr)
        return None
    except OSError as e:
        print("[!] 错误：'curl' 命令未找到。", file=sys.stderr)
        print("    请确认您的服务器已安装 curl (apt install curl / yum install curl)。", file=sys.stderr)
        print("    具体错误: " + str(e), file=sys.stderr)
        return None
    except Exception as e:
        print("[!] 获取 IP 时发生未知错误。", file=sys.stderr)
        print("    具体错误: " + str(e), file=sys.stderr)
        return None


def b64encode_str(data):
    """兼容 Python2/3 的 URL-safe Base64 编码，返回 str"""
    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    else:
        data_bytes = data
    result = base64.urlsafe_b64encode(data_bytes)
    if isinstance(result, bytes):
        result = result.decode("utf-8")
    return result.rstrip("=")


def generate_ssr_link(config):
    """
    根据给定的 SSR JSON 配置字典生成 ssr:// 订阅链接。
    """
    try:
        server = config.get("server", "")
        server_port = config.get("server_port", 8888)
        protocol = config.get("protocol", "origin")
        method = config.get("method", "aes-256-cfb")
        obfs = config.get("obfs", "plain")
        password = config.get("password", "")
        obfs_param = config.get("obfs_param", "")
        protocol_param = config.get("protocol_param", "")

        password_b64 = b64encode_str(password)

        main_part = "%s:%s:%s:%s:%s:%s" % (server, server_port, protocol, method, obfs, password_b64)

        params = {}
        if obfs_param:
            params["obfsparam"] = b64encode_str(obfs_param)
        if protocol_param:
            params["protoparam"] = b64encode_str(protocol_param)

        param_str = ""
        if params:
            param_str = "/?" + "&".join(["%s=%s" % (k, v) for k, v in params.items()])

        full_str = main_part + param_str
        ssr_link = "ssr://" + b64encode_str(full_str)

        return ssr_link
    except Exception as e:
        print("[!] 生成 SSR 链接时发生错误: " + str(e), file=sys.stderr)
        return None


def main():
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
    except Exception as e:
        print("[!] 无法读取配置文件: " + str(e), file=sys.stderr)
        sys.exit(1)

    ip = get_public_ip()
    if ip and "server" in config:
        config["server"] = ip

    ssr_link = generate_ssr_link(config)
    if ssr_link:
        print("\n[*] 生成的 SSR 链接:")
        print(ssr_link)
    else:
        print("[!] 未能生成 SSR 链接。", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://docs.microsoft.com/zh-cn/windows/win32/cimwin32prov/setdnssuffixsearchorder-method-in-class-win32-networkadapterconfiguration
# pip install wmi
# pip install pywin32

import sys
import wmi
import random


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'dhcp':
        dhcp()
    elif len(sys.argv) > 1 and sys.argv[1] == 'random':
        i = random.randint(2, 254)
        static('192.168.1.%' % i)
    else:
        args = sys.argv + ['10.10.18.73', '255.255.254.0', '10.10.18.1']
        ip, mask, gate = args[1:4]
        static(ip, mask, gate)


def dhcp():
    # Obtain network adaptors configurations
    nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
    # First network adaptor
    nic = nic_configs[0]
    # Enable DHCP
    ret = nic.EnableDHCP()
    if ret[0] != 0:
        print('set to dhcp fail with error code %s' % ret[0])
        return
    ret = nic.SetDNSServerSearchOrder()
    if ret[0] != 0:
        print('set to dns server fail with error code %s' % ret[0])
    print('set DHCP success')


def static(ip='10.10.18.73', subnetmask='255.255.254.0', gateway='10.10.18.1',
           firstDNS='1.1.1.1', secondDNS='114.114.114.114'):
    print('set static %s %s %s' % (ip, subnetmask, gateway))
    print('with dns %s %s' % (firstDNS, secondDNS))
    nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
    # First network adaptor
    nic = nic_configs[0]
    # IP address, subnetmask and gateway values should be unicode objects
    # Set IP address, subnetmask and default gateway
    # Note: EnableStatic() and SetGateways() methods require *lists* of values to be passed
    ret = nic.EnableStatic(IPAddress=[ip], SubnetMask=[subnetmask])
    if ret[0] != 0:
        print('EnableStatic error with code' % ret[0])
        return
    ret = nic.SetGateways(DefaultIPGateway=[gateway])
    if ret[0] != 0:
        print('SetGateways error with code' % ret[0])
        return
    ret = nic.SetDNSServerSearchOrder(['1.1.1.1', '114.114.114.114'])
    if ret[0] != 0:
        print('Set DNS  error with code' % ret[0])
        return
    print('set Static Addr success')


if __name__ == '__main__':
    main()

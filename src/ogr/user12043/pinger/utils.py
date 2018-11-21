#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by ME99735 on 30.10.2018 - 11:27

def print_error(e, line_number):
    print("Ignoring invalid line in input file! " + e + " in line: " + line_number)


def if_lower(ip1, ip2):
    # if code directly returns in if conditions below, function will return "None" if ips are equals.
    # So extra property added with default value
    is_lower = False
    for i in range(4):
        if int(ip1[i]) > int(ip2[i]):
            is_lower = False
        elif int(ip2[i]) > int(ip1[i]):
            is_lower = True
    return is_lower


def str_ip(ip):
    return str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(ip[3])


def compare_ip(ip1, ip2):
    if len(ip1) != len(ip2):
        return False
    equal = True
    for a in range(len(ip1)):
        if ip1[a] != ip2[a]:
            equal = False
    return equal

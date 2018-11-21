#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by ME99735 on 25/10/2018 - 16:49
# script for network operations

from ping3 import ping


def is_alive(address):
    a = ping(address)
    return str(a) != "None"


if __name__ == "__main__":
    result = is_alive("10.116.105.51")
    print(result)

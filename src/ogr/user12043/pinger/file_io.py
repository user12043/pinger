#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by ME99735 on 25/10/2018 - 16:49
# script for file operations


def read_file(file_name, n=-1, offset=0):
    try:
        file = open(file_name, "r")
        file.seek(offset)
        file_input = file.read(n)
        file.close()
        return file_input
    except FileNotFoundError as e:
        return ""


def append_file(file_name, content):
    file = open(file_name, "a")
    file.write(content)
    file.close()


def write_file(file_name, content):
    file = open(file_name, "w")
    file.write(content)
    file.close()

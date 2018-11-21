#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by ME99735 on 25/10/2018 - 16:50
# main file of application
import sys

import file_io
import net
import utils
import process_dead

properties_file = "pinger.properties"
input_file = "input.txt"
dead_file = "dead.txt"


def validate_line(interval_string):
    addresses = str(interval_string).split("-")
    syntax_error = SyntaxError("invalid line")
    value_error = ValueError("not a number input")
    type_error = TypeError("value must be between 0 - 255")
    if len(addresses) > 2 or len(addresses) == 0:
        raise syntax_error

    classes1 = addresses[0].split(".")
    if len(classes1) > 4 or len(classes1) == 0:
        raise syntax_error
    for number in classes1:
        try:
            n = int(number)
            if n < 0 or n > 255:
                raise TypeError
        except ValueError as e:
            raise value_error
        except TypeError as e:
            raise type_error

    classes2 = addresses[1].split(".")
    if len(classes2) > 4 or len(classes2) == 0:
        raise syntax_error
    for number in classes2:
        try:
            n = int(number)
            if n < 0 or n > 255:
                raise TypeError
        except ValueError as e:
            raise value_error
        except TypeError as e:
            raise type_error
    return [classes1, classes2]


def increase_ip(ip_address):
    not_increased = True
    index = 3
    while not_increased:
        if index == -1:
            ip_address = [0, 0, 0, 0]
            break
        if ip_address[index] < 255:
            ip_address[index] = ip_address[index] + 1
            if index < 3:
                while index != 3:
                    ip_address[index + 1] = 0
                    index = index + 1
            not_increased = False
        else:
            index = index - 1
    return ip_address


def get_target_list(ip1, ip2):
    target_list = []
    current_ip = ip1 if utils.if_lower(ip1, ip2) else ip2
    target_list.append(current_ip.copy())
    while utils.if_lower(current_ip, ip2):
        current_ip = increase_ip(current_ip)
        target_list.append(current_ip.copy())
    return target_list


def get_targets():
    content = file_io.read_file(input_file)
    if len(content) == 0:
        print("No input. Exiting...;")
        sys.exit(1)
    lines = str(content).splitlines()
    counter = 0
    target_list = []
    for line in lines:
        counter = counter + 1
        try:
            ips = validate_line(line)
            # convert to integer list
            ip1, ip2 = [], []
            for str_number in ips[0]:
                ip1.append(int(str_number))
            for str_number in ips[1]:
                ip2.append(int(str_number))

            # get target list
            target_list.extend(get_target_list(ip1, ip2))
        except SyntaxError as e:
            utils.print_error("Error", str(counter))
        except ValueError as e:
            utils.print_error(str(e), str(counter))
        except TypeError as e:
            utils.print_error(str(e), str(counter))
    return target_list


if __name__ == "__main__":
    # read and set properties from file
    lines = file_io.read_file(properties_file).splitlines()
    counter = 1
    for line in lines:
        try:
            property_value = line[(line.index("=") + 1):]
            if line.startswith("lost_days_interval="):
                process_dead.lost_days_interval = int(property_value)
            elif line.startswith("dead_records_file="):
                process_dead.dead_records_file = property_value
            elif line.startswith("lost_ips_file="):
                process_dead.lost_ips_file = property_value
            elif line.startswith("input_file="):
                input_file = property_value
            elif line.startswith("dead_file="):
                dead_file = property_value

        except ValueError:
            print("Error occurred when reading pinger.properties file, in line: " + str(counter))
        counter = counter + 1

    targets = get_targets()
    dead = []
    # clear dead file
    file_io.write_file(dead_file, "")
    for target in targets:
        str_target = utils.str_ip(target)
        print("pinging " + str_target + " - ", end="")
        if not net.is_alive(str_target):
            print("dead")
            dead.append(target.copy())
        else:
            print("alive")
    for dead_ip in dead:
        file_io.append_file(dead_file, utils.str_ip(dead_ip) + "\n")
    process_dead.handle_dead_time(dead)

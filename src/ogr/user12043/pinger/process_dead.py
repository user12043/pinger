#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by ME99735 on 30.10.2018 - 10:39

from datetime import datetime

import file_io
import utils

dead_records_file = "dead_records.txt"
lost_ips_file = "lost_ips.txt"
date_format = "%d.%m.%Y.%H.%M"
lost_days_interval = 60


def handle_dead_time(dead_list):
    today = datetime.today()
    # get recorded ips list
    records = file_io.read_file(dead_records_file).splitlines()
    record_list = []
    date_list = []
    for line in records:
        ip = []
        divided = line.split("-")
        ip_str = (divided[0]).split(".")
        ip_date = datetime.strptime(divided[1], date_format)
        date_list.append(ip_date)
        for str_number in ip_str:
            ip.append(int(str_number))
        record_list.append(ip)

    dead_indices = []
    # process dead ips in records
    for dead in dead_list:
        # search in records
        counter = -1
        if len(record_list) > 0:
            found = False
            for record in record_list:
                counter = counter + 1
                if utils.compare_ip(dead, record):
                    # records[counter] = utils.str_ip(dead) + "-" + str(today.strftime(date_format))
                    # new_date_list[counter] = today
                    found = True
                    dead_indices.append(counter)
                    break
            if not found:
                records.append(utils.str_ip(dead) + "-" + str(today.strftime(date_format)))
                record_list.append(dead)
                date_list.append(today)
                dead_indices.append(len(records) - 1)
        else:
            records.append(utils.str_ip(dead) + "-" + str(today.strftime(date_format)))
            record_list.append(dead)
            date_list.append(today)
            dead_indices.append(0)

    # clean alive hosts from the list
    clean_record_list = []
    clean_records = []
    clean_date_list = []
    for index in range(len(record_list)):
        if index in dead_indices:
            clean_record_list.append(record_list[index])
            clean_records.append(records[index])
            clean_date_list.append(date_list[index])

    write_content = "\n".join(map(str, clean_records))
    file_io.write_file(dead_records_file, write_content)

    counter = 0
    lost_ips = ""
    for date in clean_date_list:
        if (today - date).days > lost_days_interval:
            lost_ips += utils.str_ip(clean_record_list[counter]) + "\n"
        counter = counter + 1

    file_io.write_file(lost_ips_file, lost_ips)


if __name__ == "__main__":
    handle_dead_time(dead_records_file)

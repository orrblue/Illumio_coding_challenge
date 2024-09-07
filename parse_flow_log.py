#!/usr/bin/env python

# This script takes in a flow log file of default type, version 2 and a lookup table file
# and outputs a csv file with the tag counts and the port/protocol counts

# USAGE: python parse_flow_log.py flow_log_file lookup_table_file output_file [--measure-time]

# Author: Nitzan Orr

import csv
import socket
import argparse
import time



def main(parser):
    flow_log_file = args.flow_log_file
    lookup_table_file = args.lookup_table_file
    output_file = args.output_file
    measure_time = args.measure_time


    # Default values for version 2 VPC Flow Logs
    VERSION = 2
    NUM_FIELDS = 14

    lookup_dict = {}
    tag_dict = {}
    tag_dict['Untagged'] = 0
    combo_count = {}
    # Common protocol names to number mapping
    # https://stackoverflow.com/questions/74896954/how-to-get-the-protocol-name-in-pyshark
    proto_names={v:k[8:] for (k,v) in vars(socket).items() if k.startswith('IPPROTO')}

    start = None
    if measure_time:
        start = time.time()

    # Populate tag dictionaries from lookup table
    with open(lookup_table_file, newline='') as csvfile:
        stripped_lines = (line.strip() for line in csvfile)
        reader = csv.reader(stripped_lines)
        try:
            header = next(reader)
        except StopIteration:
            print(f"Empty lookup table: {lookup_table_file}")
            return
        for row in reader:
            if row:
                if len(row) != 3 or not row[0].isdigit():
                    print(f"Invalid lookup table entry: {row}")
                    continue
                dstport = row[0].strip()
                protocol = row[1].strip()
                tag = row[2].strip()
                if lookup_dict.get((dstport, protocol)):
                    print(f"Tried inserting {tag} but duplicate entry found: {dstport}, {protocol} -> {lookup_dict.get((dstport, protocol))}")
                
                lookup_dict[(dstport, protocol)] = tag
                combo_count[(dstport, protocol)] = 0
                tag_dict[tag] = 0


    # Extract dstport and protocol from flow logs
    with open(flow_log_file, newline='') as csvfile:
        stripped_lines = (line.strip() for line in csvfile)
        reader = csv.reader(stripped_lines, delimiter=' ')
        for row in reader:
            if row:
                version = row[0].strip()
                if not version.isdigit() or int(version) != VERSION:
                    print(f"Invalid flow log version. Expected {VERSION}: {row}")
                    continue
                if len(row) != NUM_FIELDS:
                    print(f"Invalid flow log entry. Expected length {NUM_FIELDS}: {row}")
                    continue
                dstport = row[6].strip()
                protocol = row[7].strip()
                if not (dstport.isdigit() or dstport == '-') or not (protocol.isdigit() or protocol == '-'):
                    print(f"Invalid flow log entry: {row}")
                    continue  
                if protocol.isdigit():
                    protocol = proto_names[int(protocol)].lower()
                if (dstport, protocol) in lookup_dict:
                    tag = lookup_dict[(dstport, protocol)]
                    tag_dict[tag] += 1
                else:
                    tag_dict['Untagged'] += 1

                if (dstport, protocol) in combo_count:
                    combo_count[(dstport, protocol)] += 1
                else:
                    combo_count[(dstport, protocol)] = 1

    # Output file with tag counts and port/protocol counts
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Tag', 'Count'])
        for key, value in tag_dict.items():
            if value > 0 and key != 'Untagged':
                writer.writerow([key, value])
        if tag_dict['Untagged'] > 0:
            writer.writerow(['Untagged', tag_dict['Untagged']])
        
        writer.writerow([])
        writer.writerow(['DstPort', 'Protocol', 'Count'])
        for key, value in combo_count.items():
            if value > 0:
                writer.writerow([key[0], key[1], value])

    if measure_time:
        end = time.time()
        print(f"\nTime taken: {end - start:.2f} seconds")

    print(f"\nOutput written to {output_file} \n")

if __name__ == '__main__':

    # read the file names from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('flow_log_file', type=str, help='The flow log file to parse')
    parser.add_argument('lookup_table_file', type=str, help='The lookup table file to use')
    parser.add_argument('output_file', type=str, help='The output file to write the results to')
    parser.add_argument('--measure-time', action='store_true', help='Measure the time taken by the function')
    args = parser.parse_args()
    main(args)

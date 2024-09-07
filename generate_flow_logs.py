
# This file generates a flow log file with random data.
# It reports the number of tags that should be applied based on
#   the lookup table in lookup_test_1.txt   
# The number of logs can be specified 

import random
import time

NUM_LOGS = 100000

COMMON_PROTOCOLS = {0: 'HOPOPTS', 1: 'ICMP', 2: 'IGMP', 3: 'GGP', 4: 'IPIP', 6: 'TCP', 8: 'EGP', 12: 'PUP', 17: 'UDP', 
             22: 'IDP', 29: 'TP', 36: 'XTP', 41: 'IPV6', 43: 'ROUTING', 44: 'FRAGMENT', 46: 'RSVP', 47: 'GRE', 
             50: 'ESP', 51: 'AH', 58: 'ICMPV6', 59: 'NONE', 60: 'DSTOPTS', 63: 'HELLO', 77: 'ND', 80: 'EON', 
             103: 'PIM', 108: 'IPCOMP', 132: 'SCTP', 255: 'RAW'}

COMMON_PORTS = [20, 21, 22, 23, 25, 53, 80, 110, 123, 143, 443, 3306, 3389, 5432, 8080]

tag_counts = {}
tag_counts['sv_P2'] = 0
tag_counts['SV_P3'] = 0
tag_counts['sv_P4'] = 0
tag_counts['email'] = 0
tag_counts['Email'] = 0

def generate_flow_log(include_missing_data=True):
    global tag_counts

    version = 2
    account_id = "123456789012"
    interface_id = f"eni-{random.randint(1000000000, 9999999999)}"
    srcaddr = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    dstaddr = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    # Use common ports with higher probability
    srcport = random.choice(COMMON_PORTS) if random.random() < 0.8 else random.randint(0, 65535)
    dstport = random.choice(COMMON_PORTS) if random.random() < 0.8 else random.randint(0, 65535)
    
    protocol = random.choice(list(COMMON_PROTOCOLS.keys())) 
    packets = random.randint(1, 1000)
    bytes = random.randint(64, 1500) * packets
    start = int(time.time())
    end = start + random.randint(1, 600)
    action = random.choice(["ACCEPT", "REJECT"])
    log_status = random.choice(["OK", "NODATA", "SKIPDATA"])

    if include_missing_data:
        # Randomly choose fields to represent as missing
        fields = [account_id, interface_id, srcaddr, dstaddr, srcport, dstport, protocol, packets, bytes, start, end, action]
        for i in range(len(fields)):
            if random.random() < 0.05:  # 5% chance of being missing
                fields[i] = "-"
        account_id, interface_id, srcaddr, dstaddr, srcport, dstport, protocol, packets, bytes, start, end, action = fields



    # known combo that should be tagged 
    if dstport == 31 and protocol == 17:
        tag_counts['SV_P3'] += 1
    elif dstport == 22 and protocol == 6:
        tag_counts['sv_P4'] += 1
    elif dstport in [110, 993] and protocol == 6:
        tag_counts['email'] += 1
    elif dstport in [143] and protocol == 6:
        tag_counts['Email'] += 1
    elif (dstport == 68 and protocol == 17) or (dstport == 443 and protocol == 6):
        tag_counts['sv_P2'] += 1


    return f"{version} {account_id} {interface_id} {srcaddr} {dstaddr} {srcport} {dstport} {protocol} {packets} {bytes} {start} {end} {action} {log_status}"


# Write to file:
with open('flow_log_test_2.txt', 'w') as file:
    for _ in range(NUM_LOGS):
        file.write(generate_flow_log() + '\n')

# Print the expected tag counts, to be cross-verified with the output of parse_flow_log.py
for key, value in tag_counts.items():
    print(key, value)

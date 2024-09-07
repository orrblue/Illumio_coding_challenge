Illumio Technical Assessment README


Requirements:
Python 3.11

Tested on MacOS 14.6.1, but should work on non-Unix-based systems as well

RUNNING:
python3 parse_flow_log.py flow_log_file lookup_table_file output_file [--measure-time]

RUNNING WITH INCLUDED TEST FILES:
python parse_flow_log.py flow_log_test_2.txt lookup_test_3.txt output_test_9.txt --measure-time


ASSUMPTIONS:
This code assumes the following statements are true:
1. Flow log files contains only default version 2 logs
2. The flow logs' fields are space-separated in a plaintext ascii file
3. The lookup table file contains a header row with 3 comma-separeted columns an ascii plaintext
4. The look up file can have up to 10,000 mappings
5. The flow log file size can be up to 10MB
6. The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample
7. The matches are case insensitive 
8. The output file is a hybrid CSV, where the first part is a header with 2 columns (tag, count) and the second part has a header and 3 columns (DstPort,Protocol,Count)
9. The output file does not show tags with fewer than 1 match
10. Only the following protocols are supported due to being common and available in the Python socket package: {0: 'HOPOPTS', 1: 'ICMP', 2: 'IGMP', 3: 'GGP', 4: 'IPIP', 6: 'TCP', 8: 'EGP', 12: 'PUP', 17: 'UDP', 
             22: 'IDP', 29: 'TP', 36: 'XTP', 41: 'IPV6', 43: 'ROUTING', 44: 'FRAGMENT', 46: 'RSVP', 47: 'GRE', 
             50: 'ESP', 51: 'AH', 58: 'ICMPV6', 59: 'NONE', 60: 'DSTOPTS', 63: 'HELLO', 77: 'ND', 80: 'EON', 
             103: 'PIM', 108: 'IPCOMP', 132: 'SCTP', 255: 'RAW'}
11. The run time of the code is to be under 1 second for a 10MB input logs file with 10,000 mappings on a typical laptop.

TESTS:
The following tests were performed:
1. Tested edge cases where files are empty, uneven spacing, unknown values "-", and malformed logs or lookup entries.
2. Performed manual checking on provided sample input. Sample output was not used as it appears to be an example, not a ground truth.
3. Created randomized flow log file generator to create and test 10MB file. Includes missing data points: "-"
4. Created ~10,000 mapping look-up file using output from running code on 10MB file
5. Timed the code on 10MB input with ~10,000-entry look-up file mappings: ~0.18 seconds
6. Along with timing, I also checked a few tags to ensure the program found the accurate number of those tags, as were generated. 

POSSIBLE IMPROVEMENTS: 
1. Distributing the work across threads or processors
2. More robust error checking and handling for additional ascii characters, large or negative numbers beyond the Flow Log spec.
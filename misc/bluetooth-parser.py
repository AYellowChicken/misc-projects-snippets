'''
=== BTSnoop decoder - Decode and print out packets captured in a BTSnoop file ===

Usage:
binary.py [-i <file>] [--output <folder>]

Options:
    -i, --input <file>    input BTSnoop file [default: /mnt/d/Downloads/ch18.bin]
    -o, --output <folder> the output folder
    -h, --help            help

'''

from docopt import docopt
from datetime import datetime
import logging
import struct

# Terminal colors


class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


datalink_list = {
    1001: "Un-encapsulated HCI (H1)",
    1002: "HCI UART (H4)",
    1003: "HCI BSCP",
    1004: "HCI Serial (H5)",
}


def print_datalink_type(datalink_type):
    if datalink_type in datalink_list.keys():
        print(f'Datalink {datalink_type} : {datalink_list[datalink_type]}')
    else:
        if datalink_type >= 0 and datalink_type <= 1000:
            print(f'Datalink {datalink_type} : Reserved')
        elif datalink_type >= 1005:
            print(f'Datalink {datalink_type} : Unassigned')
        else:
            print(f'Datalink {datalink_type} : Invalid')


pkt_num = 0


def parse_packet(file):
    global pkt_num
    pkt_num += 1

    # Original length
    og_length = file.read(4)
    if len(og_length) != 4:
        print("End of file reached. Exitting...")
        return False

    else:
        og_length = struct.unpack(">I", og_length)[0]

    # Included length
    inc_length = struct.unpack(">I", file.read(4))[0]

    print(f'\n{bcolors.GREEN}Packet n°{pkt_num}{bcolors.END}\nOriginal Length : {og_length} - Included Length {inc_length}')

    # Packet flags
    flags = file.read(4)
    tx_rx = "Sent" if flags[3] & 0x1 == 1 else "Received"
    cmd_data = "Command" if flags[3] & 0x2 == 2 else "Data"
    print(f'{tx_rx} {cmd_data}')

    # Cumulative Drop
    drops = struct.unpack(">I", file.read(4))[0]
    if drops > 0:
        print(f'{bcolors.RED}{drops} dropped{bcolors.END}')
    else:
        print(f'{drops} dropped')

    # Timestamp
    timestamp = struct.unpack(">q", file.read(8))[0]
    print(f"Timestamp {timestamp}")

    # Data
    raw_data = file.read(inc_length)
    data = raw_data.hex(" ")
    print(f'Data :\n{data}')

    if pkt_num == 22:
        with open("return.txt", "wb") as outputfile:
            outputfile.write(raw_data)

    return True


if __name__ == "__main__":
    args = docopt(__doc__, version=0.1)
    print(f"\n {bcolors.BLUE}====== BTSnoop Parser ======{bcolors.END} \n")
    input = args['--input']
    output_folder = args['--output']
    time = datetime.now().strftime("%Y-%m-%d_%Hh%M")

    try:
        with open(input, "rb") as file:

            # File Header
            header = file.read(8)
            if header != b'btsnoop\x00':
                logging.exception(
                    f"Not a BTSnoop trace file : Header is {header}")
                exit()
            else:
                print(f'HEADER : {header.hex(" ")}')

            # Version
            version = file.read(4)
            version = struct.unpack('>I', version)[0]
            if version != 1:
                logging.exception(
                    f"Version {version} is used instead of 1. Quitting...")
                exit()
            else:
                print(f"VERSION : {version}")

            # Datalink type
            datalink_type = file.read(4)
            datalink_type = struct.unpack(">I", datalink_type)[0]
            print_datalink_type(datalink_type)

            while True:
                more_pkts = parse_packet(file)
                if not more_pkts:
                    break

    except FileNotFoundError as e:
        logging.exception("Input file " + input + " invalid.")
        exit()

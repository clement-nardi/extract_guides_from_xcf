#!/bin/env python3

# extract list of guide coordinates from a .xcf file

import sys
import argparse

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Extract list of guide coordinates from a .xcf file")
    argparser.add_argument("xcf_file", help="The .xcf file to extract guide coordinates from")
    args = argparser.parse_args()

    # read file byte by byte
    last4bytes = 0
    with open(args.xcf_file, "rb") as f:
        while True:
            nextbyte = f.read(1)
            last4bytes = ((last4bytes << 8) & 0x00000000FFFFFFFF) | int.from_bytes(nextbyte, "big") 
            
            if last4bytes == 18:
                # PROP_GUIDES
                nb_bytes = int.from_bytes(f.read(4), "big")
                if nb_bytes % 5 != 0:
                    print(f"Error: nb_bytes % 5 != 0 -> exiting")
                    exit(1)
                nb_guides = int(nb_bytes / 5)
                for i in range(nb_guides):
                    coord = int.from_bytes(f.read(4), "big")
                    orientation = int.from_bytes(f.read(1), "big")
                    orientation_str = "Unknown"
                    if orientation == 1:
                        orientation_str = "Horizontal"
                    elif orientation == 2:
                        orientation_str = "Vertical"
                    else:
                        print(f"Unknown orientation: {orientation} -> exiting")
                        exit(1)

                    print(f"Guide #{i}: {orientation_str} - {coord}")
                exit(0)


#!/usr/bin/python3.6

import argparse
import os
import sys
import tarfile
import datetime
import subprocess

def compress(dir):
    with tarfile.open(name_of_tarfile, "w") as tar:
        tar.add(dir, arcname = base_dir)

def uncompress(file):
    if tarfile.is_tarfile(file):
        with tarfile.open(file, "r") as tar:
            tar.extractall()
        sys.exit(0)
    else:
        print(file, " is not a tar file")
        sys.exit(1)

about = "This script will tar a dir that is passed to it.  Same as 'tar -cf dir'"

parser = argparse.ArgumentParser(description = about)
parser.add_argument("directory", help = "You must pass a DIR", action = "store")
parser.add_argument("-u", "--uncompress", help = "Use to uncompress tar file",
                        action = "store_true", dest = "uncompress")

args = parser.parse_args()
directory = args.directory
uncompress_flag = args.uncompress

if uncompress_flag:
    uncompress(directory)
else:
    base_dir = directory.split("/")
    if base_dir[-1] == "":
        base_dir = base_dir[-2]
    else:
        base_dir = base_dir[-1]

    today = str(datetime.datetime.now()).replace(" ", "__").replace(":", "_")
    name_of_tarfile = base_dir + "-" +today + ".tar"
    if directory[-1] is not "/":
        directory = directory + "/"

    if not os.path.isdir(directory):
        print("You did not pass a directory to this scirpt \nPlease use 'backup_dir -h' for more details\n")
        sys.exit(1)
    compress(directory)

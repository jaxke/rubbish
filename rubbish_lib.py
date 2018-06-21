import os
import subprocess
import argparse
from pdb import set_trace as st
import sys
import time
import json
import traceback

'''
Library of functions used by the wrapper script
'''

SRC_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
BIN = SRC_DIR + "bin/"
LOG = SRC_DIR + ".log"


if __name__ == "__main__":
    print("This file is a library and can't be used by itself.")
    sys.exit(1)


# Return bin directory size
def get_bin_size():
    return subprocess.check_output(['du','-sh', get_bin()]).split()[0].decode('utf-8')


# Make sure dir exists each time it is accessed
def get_bin():
    if not os.path.isdir(BIN):
        os.mkdir(BIN)
    return BIN


# Files are stored as incrementing integers as id, this function finds the last
# id and the function calling it will increment it if it is mv'ing another file
def get_last_id():
    ls = sorted(os.listdir(get_bin()))
    if len(ls) == 0:
        return 0
    for f in reversed(ls):
        if f.isnumeric():   # Make sure to skip files that are put there by accident
            return int(f)


def rm(files):
    del_count = 0
    for file in files:
        # If argument is not an abs path user is trying to put a file into bin from cwd
        if file[0] not in ["~", "/"]:
            file = os.getcwd() + "/" + file
        try:
            ret_mv = os.rename(file, get_bin() + str(get_last_id() + 1))
            mark_deletion(file)
            del_count += 1
        except FileNotFoundError:
            print(file + " does not exist. Skipping.")
    return del_count


# Write data to JSON so the program can keep track of it
def mark_deletion(file):
    time_date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    open(LOG, "a").close()  # Make sure the LOG file exists(recreates it otherwise)
    with open(LOG, "r") as log_read:
        try:
            old_contents = json.load(log_read)
        except json.decoder.JSONDecodeError:    # Bad data
            old_contents = None
    with open(LOG, "w") as log_write:
        # Format {"1": {filename: "/home/user/file", timedate: str(time_and_date)}}
        dump = {str(get_last_id()): {"filename": file, "timedate": time_date}}
        try:
            # Merge new entry to the old JSON data(append to existing data)
            new_contents = dict(old_contents, **dump)
        # raises TypeError if old_contents == None
        except TypeError:
            new_contents = dump
        json.dump(new_contents, log_write)


# Remove entry from JSON upon restoring files(JSON entries must be gone if files are removed from bin)
def mark_restoration(file_id):
    del_id = ""
    with open(LOG, "r") as log_read:
        json_contents = json.load(log_read)
    for item in json_contents:
        if item == file_id:
            # Can't del from within the loop that's iterating over it
            del_id = item
            break
    del json_contents[del_id]
    with open(LOG, "w") as log_write:
        json.dump(json_contents, log_write)  # Write data back to JSON(without the entry we just deleted)


def bin_contents():
    try:
        with open(LOG, "r") as log_read:
            json_contents = json.load(log_read)
            return json_contents
    except FileNotFoundError:
        return


def restore_by_filename(files):
    files_restored = 0
    for file in files:
        if restore(file):
            files_restored += 1
    return files_restored


def restore_by_index(indexes):
    files_restored = 0
    files_in_bin = bin_contents()
    for index in indexes:
        try:
            file_to_restore = files_in_bin.get(index, None)['filename']
        except TypeError:
            print("This file was not found in the bin") # This should not happen
            return
        # if file exists in bin
        if file_to_restore:
            if restore(file_to_restore):
                files_restored += 1
    return files_restored


def restore(file_to_restore):
    files_in_bin = bin_contents()
    for item in files_in_bin:
        if files_in_bin[item]['filename'] == file_to_restore:
            file_id = item
            try:
                os.rename(get_bin() + str(file_id), file_to_restore)
                mark_restoration(file_id)
                return True
            except FileNotFoundError as e:
                ex, val, tb = sys.exc_info()
                #traceback.print_exception(ex, val, tb)
                print("File was not found in the bin.")

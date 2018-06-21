import os
import subprocess
import argparse
from pdb import set_trace as st
import sys
import time
import json


SRC_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
BIN = SRC_DIR + "bin/"
LOG = SRC_DIR + ".log"


if __name__ == "__main__":
    print("This file is a library and can't be used by itself.")
    sys.exit(1)


def get_last_id():
    ls = sorted(os.listdir(BIN))
    if len(ls) == 0:
        return 1
    for f in reversed(ls):
        if f.isnumeric():
            return int(f) + 1


def rm(files, curr_dir):
    del_count = 0
    if not os.path.isdir(BIN):
        os.mkdir(BIN)
    for file in files:
        if file[0] not in ["~", "/"]:
            file = curr_dir + "/" + file
        filename = file.split("/")[-1]
        try:
            mark_deletion(file)
            ret_mv = os.rename(file, BIN + str(get_last_id()))
            del_count += 1
        except FileNotFoundError:
            print(file + " does not exist. Skipping.")
    return del_count


def mark_deletion(file):
    time_date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    open(LOG, "a").close()
    with open(LOG, "r") as log_read:
        try:
            old_contents = json.load(log_read)
        except json.decoder.JSONDecodeError:
            old_contents = None
    with open(LOG, "w") as log_write:
        dump = {str(get_last_id()): {"filename": file, "timedate": time_date}}
        try:
            new_contents = dict(old_contents, **dump)
        # raises TypeError if old_contents == None
        except TypeError:
            new_contents = dump
        json.dump(new_contents, log_write)


def mark_restoration(file_id):
    del_id = ""
    with open(LOG, "r") as log_read:
        json_contents = json.load(log_read)
    for item in json_contents:
        if item == file_id:
            # Can't del from within the loop that's iterating over it
            del_id = json_contents[item]
            break
    del json_contents[del_id]
    with open(LOG, "w") as log_write:
        json.dump(json_contents, log_write)

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
                os.rename(BIN + str(file_id), file_to_restore)
                mark_restoration(file_id)
                return True
            except Exception as e: # # TODO
                st()
                print("Exception ", e)
                return
        print("File was not found in the bin. Check that your argument ")

import rubbish
import sys


if __name__ == "__main__":
    files_in_bin = rubbish.bin_contents()

    if not files_in_bin:
        print("Bin is empty!")

    for item in files_in_bin:
        print("{0}: {1} (DELETED AT {2})".format(item, files_in_bin[item]['filename'], files_in_bin[item]['timedate']))

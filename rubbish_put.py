import rubbish
import sys
import os


files = sys.argv[1:]
curr_dir = os.getcwd()
ret = rubbish.rm(files, curr_dir)
print(ret, "out of", len(files), "files moved to bin.")

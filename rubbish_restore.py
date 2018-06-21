import rubbish
import sys
from pdb import set_trace as st

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: rubbish_restore [files] | [indexes]")
        sys.exit(1)

    if len(rubbish.bin_contents()) == 0:
        print("Bin is empty!")
        sys.exit(0)

    for arg in args:
        if arg[0] != "/" or not arg.isnumeric():
            print("You must specify an absolute path or provide the id of the file(rubbish-list)")
            sys.exit(1)

    isnumeric = True
    for arg in args:
        if not arg.isnumeric():
            isnumeric = False
            break

    restored = 0
    # If all args are numeric
    if isnumeric:
        restored = rubbish.restore_by_index(args)
    # If at least one is not
    else:
        restored = rubbish.restore_by_filename(args)

    print("Restored", restored, "out of", len(args), "files.")

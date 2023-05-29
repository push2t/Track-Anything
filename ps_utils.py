from tools import ps
import argparse
import glob
import os
import stat
import shutil
import tools.ps

parser = argparse.ArgumentParser()
parser.add_argument("--dirstack_basedir", required=True, help="this should be a directory of subdirectories, each of which is named for your target psd and contains images to be loaded as layers", required=False)
parser.add_argument("--psd_fn_suffix", help="append this to the subdirectory name before the .psd, optional", required=False)
args = parser.parse_args()

files = glob.glob(args.dirstack_basedir + "/*")
if len(files) == 0:
    raise ValueError("could not dirstack from dirstack_basedir %s, was empty" % (args.dirstack_basedir))
    
for f in files:
    mode = os.lstat(f).st_mode
    if stat.S_ISDIR(mode):
        _, shortname = os.path.split(f)
        print(f + " is directory, using " + shortname + " as document name")

        if args.psd_fn_suffix:
            psd = f + "/" + shortname + args.psd_fn_suffix + ".psd"
        else:
            psd = f + "/" + shortname + ".psd"

        print("stacking contents of %s into %s", f, psd)
        tools.ps.subdir_stack_to_psd(f, psd)

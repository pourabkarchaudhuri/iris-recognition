##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse, os
import glob
from tqdm import tqdm
from time import time
from scipy.io import savemat
from multiprocessing import cpu_count, Pool

from fnc.extractFeature import extractFeature


#------------------------------------------------------------------------------
#	Argument parsing
#------------------------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--data_dir", type=str, default="CASIA1/",
					help="Path to the directory containing CASIA1 images.")

parser.add_argument("--temp_dir", type=str, default="./templates/CASIA1/",
					help="Path to the directory containing templates.")

parser.add_argument("--n_cores", type=int, default=cpu_count(),
					help="Number of cores used for enrolling template.")

args = parser.parse_args()


##-----------------------------------------------------------------------------
##  Pool function
##-----------------------------------------------------------------------------
def pool_func(file):
	template, mask, _ = extractFeature(file, use_multiprocess=False)
	basename = os.path.basename(file)
	out_file = os.path.join(args.temp_dir, "%s.mat" % (basename))
	savemat(out_file, mdict={'template': template, 'mask': mask})


##-----------------------------------------------------------------------------
##  Execution
##-----------------------------------------------------------------------------
def execute():
	start = time()

	# Check the existence of temp_dir
	if not os.path.exists(args.temp_dir):
		print("makedirs", args.temp_dir)
		os.makedirs(args.temp_dir)

	# Get list of files for enrolling template, just "xxx_1_x.jpg" files are selected
	directory = os.path.join(os.getcwd(), args.data_dir)
	print("Data directory : {}".format(directory))
	# files = glob(os.path.join(directory, "*_1_*.jpg"))
	# files = glob.glob(os.path.join('*//*.jpg'))
	files = [f for f in glob.glob(directory + "**/*.jpg", recursive=True)]
	# glob.glob()
	print(files)
	n_files = len(files)
	print("Number of files for enrolling:", n_files)

	# Parallel pools to enroll templates
	print("Start enrolling...")
	pools = Pool(processes=args.n_cores)
	for _ in tqdm(pools.imap_unordered(pool_func, files), total=n_files):
		pass

	end = time()
	print('\n>>> Enrollment time: {} [s]\n'.format(end-start))


if __name__ == '__main__':    
    execute()
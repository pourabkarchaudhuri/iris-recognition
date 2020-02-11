##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse, os
from time import time

from fnc.extractFeature import extractFeature
from fnc.matching import matching


#------------------------------------------------------------------------------
#	Argument parsing
#------------------------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str,
                    help="Path to the file that you want to verify.")

parser.add_argument("--temp_dir", type=str, default=os.path.join(os.getcwd(), "templates", "CASIA1/"),
					help="Path to the directory containing templates.")

parser.add_argument("--thres", type=float, default=0.38,
					help="Threshold for matching.")

args = parser.parse_args()


##-----------------------------------------------------------------------------
##  Execution
##-----------------------------------------------------------------------------
# Extract feature
def execute(image_file):
	# start = time()
	final_result = []
	print('>>> Start verifying {}\n'.format(os.path.join(os.getcwd(), image_file)))
	
	template, mask, file = extractFeature(os.path.join(os.getcwd(), image_file))

	# print("Template recieved : {}".format(template))
	# print("Mask recieved : {}".format(mask))
	print("Threshold recieved : {}".format(args.thres))
	# Matching
	print("Templates path : {}".format(args.temp_dir))
	result = matching(template, mask, os.path.join(os.getcwd(), "templates", "CASIA1/"), 0.35000000)

	if result == -1:
		print('>>> No registered sample.')

	elif result == 0:
		print('>>> No sample matched.')

	else:
		print('>>> {} samples matched (descending reliability):'.format(len(result)))
		for res in result:
			# print("\t", res)
			# print(int(os.path.split(res)[len(os.path.split(res))-1].split("_",1)[0]))
			# print(os.path.split(res)[len(os.path.split(res))-1].split(".",2)[0])
			# print(os.path.split(res)[len(os.path.split(res))-1].split(".",2)[1])
			image = os.path.join( "static", "CASIA1", str(int(os.path.split(res)[len(os.path.split(res))-1].split("_",1)[0])), os.path.split(res)[len(os.path.split(res))-1].split(".",2)[0] + "." + os.path.split(res)[len(os.path.split(res))-1].split(".",2)[1])
			final_result.append({"path": image, "id": os.path.split(res)[len(os.path.split(res))-1].split("_",1)[0]})
			# print(os.path.split(res)[len(os.path.split(res))-1])

	# print(final_result)
	# Time measure
	# end = time()
	# print('\n>>> Verification time: {} [s]\n'.format(end - start))
	return final_result

# if __name__ == '__main__':    
#     execute()
"""
This script augments the dataset,
going from 2600 to 21000 images
This allows the  dataset to be stored 
on GitHub, and easily downloaded.
It also saves it as h5 file
"""

import os
import cv2
import imutils
import numpy as np
from random import shuffle
import h5py

imageSize = 128

# Generates 4 flips of the images
def flip():
	files = [file for file in os.listdir("Images") if file.endswith(".png") or file.endswith(".jpg")]
	
	for i, file in enumerate(files):
		print "Flipping file {}/{}".format(i,len(files))

		img = cv2.imread("Images/"+file,-1)
		rflip = cv2.flip(img,1)
		vflip = cv2.flip(img,0)
		rvflip = cv2.flip(rflip,0)

		cv2.imwrite("Flipped/"+file[:-4]+"_.png",img)
		cv2.imwrite("Flipped/"+file[:-4]+"_r.png",rflip)
		cv2.imwrite("Flipped/"+file[:-4]+"_v.png",vflip)
		cv2.imwrite("Flipped/"+file[:-4]+"_rv.png",rvflip)

# Generates 2 rotations of the images
def rotate():
	files = [file for file in os.listdir("Flipped") if file.endswith(".png") or file.endswith(".jpg")]

	# 2 rotations * 4 flips = 8 possibilites
	for index, file in enumerate(files):
		print "Rotating file {}/{}".format(index,len(files))
		img = cv2.imread("Flipped/"+file,-1)
		cv2.imwrite("Rotated/"+file[:-4]+"_0.png",img)
		img = np.rot90(img)
		cv2.imwrite("Rotated/"+file[:-4]+"_90.png",img)

# Save h5 dataset
def save():
	#Load, normalize and reshape
    files = os.listdir("Rotated/")
    files = [file for file in files if file.endswith(".png")]
  
    shuffle(files)
    X = []
    for i, file in enumerate(files):
    	print "Adding file {}/{}".format(i,len(files))
        img = cv2.imread("Rotated/"+file, -1)

        # Convert grayscale to RGB
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # Resize to desired size and normalize
        img = cv2.resize(img,(imageSize,imageSize))
        img = img.astype(float)/255.
        X.append(img)

    # Convert to numpy array
    X = np.array(X)

    # 10% for testing
    testProportion = 0.1
    trainNb = int(X.shape[0]*(1-testProportion))
    testNb = X.shape[0] - trainNb

    print "Splitting dataset in X_train({}) and X_test({})...".format(trainNb,testNb)
    # Split train test
    X_train = X[:trainNb]
    X_test = X[-testNb:]

    #Save at hdf5 format
    print "Saving dataset in hdf5 format... - this may take a while"
    h5f = h5py.File("coins.h5", 'w')
    h5f.create_dataset('X_train', data=X_train)
    h5f.create_dataset('X_test', data=X_test)
    h5f.close()

if __name__ == "__main__":
	print "This script creates 21208k images from the base 2652"
	print "Make sure the folders Rotated and Flipped exist"
	#flip()
	#rotate()
	save()



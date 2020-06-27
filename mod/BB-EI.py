import argparse as arg
import datetime
import os
from xml.etree import ElementTree as ET
from xml.dom import minidom


import tensorflow as tf
import cv2
import numpy as np




photopath = "lol.jpg"
output_list = "train" + str(datetime.datetime) + ".txt"
#do they create val for us?
refDir = {}
windowName = "viewer"
ButtonNext = "Next Sample"
ButtonPrev = "Previous Sample"
ButtonAdd = "Add boundingbox"

colorblack = (0,0,0)
font = cv2.FONT_HERSHEY_SIMPLEX

INPUT_FOLDER_PATH = "input/image"
LOADER_PATH = "input/imageloader.xml"

filename = None #name of current file
source = None #path to current file
files = None #List of filenames
file = None #current file dictionary
f = None #open()ed file

status = "ready"
infoImg = None #background for application
n_bndname = 0

i = 1 #iterator in input folder
currentImgRAM = None
currentImg = None #viewing image array
currentClass = 0 #selecting class in trackbar
currentClassList = None #array of available class
num_class = 10 #len of currentClassList


#definitions for cropping
refPt = []
refPti = ()
cropping = False



#def imageloader_export():
	#for filename in os.listdir(INPUT_FOLDER_PATH):
def nothing(x):
	pass

def imageloader_importpath():
	
	global file
	#This should only be run once.
	"""
	imageloader = {}
	imageloader['data'] = {}
	imageloader['object'] = {}
	imageloader['data'] = {
		'date_created': str(datetime.datetime.now()),
		'cool': 'yes'
		}


	with open("input/imageloader.xml", 'w+') as f:
		json.dump(imageloader, f,sort_keys=True, indent=4, separators=(',', ': '))
	"""
	file = ET.Element('data')
	date_created = ET.SubElement(file,'date_created')
	date_created.text = str(datetime.datetime.now())
	objcat = ET.SubElement(file, 'objects')
	"""
	bnd1 = {'directory': 'd:/dir2/openhand/input/image/log.jpg','xmin': '112', 'ymin': '86', 'xmax': '200', 'ymax': '481'}
	obj1 = ET.SubElement(objcat, 'the-world-can-be-a-better-place.jpg',bnd1)
	obj2 = ET.SubElement(objcat, 'pornobit.jpg')
	print(        len(list( root.find('object').find('pornobit.jpg').iter() ))               )
	print(root.find('object').find('the-world-can-be-a-better-place.jpg').attrib)
	
	"""
	f = ET.ElementTree(file)
	f.write(LOADER_PATH)

def mainUI():

	
	print("If this line repeats more than once, there's an overflow")
	global i, refPt, status, source, file, filename, infoImg, n_bndname, currentClass, cropping, currentImg, currentImgRAM

	StartWindow()


	files = os.listdir(INPUT_FOLDER_PATH)
	assert len(files) > 0, "No files for viewing"
	
	#with open(LOADER_PATH,encoding="utf8", mode='r+') as f:
	try:
		f = ET.parse(LOADER_PATH)
	except ET.ParseError:
		imageloader_importpath()
	except FileNotFoundError:
		file = ET.Element('data')
		f = ET.ElementTree(file)
		f.write(LOADER_PATH)
	
	f = ET.parse(LOADER_PATH)
	file = f.getroot()
	
	i=0
	while(True):
		currentClass = cv2.getTrackbarPos('Class', windowName)
		key = cv2.waitKey(1)
		i = min(max(i,0),int(len(files)-1))
		
		#main display for the viewer
		source = str(INPUT_FOLDER_PATH + "/" + files[i])
		if cropping == False:
			currentImg = cv2.imread(source)
			currentImgRAM=currentImg
			cv2.imshow(windowName, currentImg)
		else:
			currentImgRAM=currentImg
			cv2.imshow(windowName, currentImgRAM)
			
		filename = str(files[i])
		

		#info window
		infoImg = np.full((400,1500,3),0,np.uint8)
		desImg1 = str("filename: "+files[i])
		desImg2 = "order: {0} of {1} images".format(str(i+1),str(len(files)))
		desImg3 = "bndboxes: {}".format(n_bndname)
		desImg4 = "status: " + status
		cv2.putText(infoImg, desImg1, (10,100), font,1, (0,255,0), 2, cv2.LINE_AA)
		cv2.putText(infoImg, desImg2, (10,140), font,1, (0,255,0), 2, cv2.LINE_AA)
		cv2.putText(infoImg, desImg3, (10,190), font,1, (0,255,0), 2, cv2.LINE_AA)
		cv2.putText(infoImg, desImg4, (10,240), font,1, (0,255,0), 2, cv2.LINE_AA)
		cv2.imshow("Info", infoImg)


		if len(refPt) == 2:
			xmin,ymin,xmax,ymax = findmaxmin()
			#roiframe = currentImg[xmin:xmax,ymin:ymax]
			status = "processed new bndboxd {},{},{},{}".format(xmin,ymin,xmax,ymax)
			
		if not cropping: 
			cv2.setMouseCallback(windowName, mousecropping)

		if key == ord('a'):
			i-=1
		
		elif key == ord('d'):
			i+=1
		#reload list
		elif key == ord('r'):
			files = os.listdir(INPUT_FOLDER_PATH)
		#convert list
		elif key == ord('t'):
			print("convert format")
		#exit key: ESC
		elif key == 27:
			break

	#json.dump(file,f,sort_keys=True, indent=4, separators=(',', ': '))
	#f.close()
	f.write(LOADER_PATH)
	cv2.destroyAllWindows()

def findmaxmin():
	global refPt
	assert len(refPt) == 2, "Not enough ref points for postprocessing"
	xmin = min(refPt[0][0],refPt[1][0])
	ymin = min(refPt[0][1],refPt[1][1])
	xmax = max(refPt[0][0],refPt[1][0])
	ymax = max(refPt[0][1],refPt[1][1])
	return xmin,ymin,xmax,ymax
	
def addbndtoobject():
	objname = filename
	global refPt, file, n_bndname, currentClass
	print(currentClass)
	assert len(refPt) == 2, "Not enough reference points for adding bounding box."
	xmin,ymin,xmax,ymax = findmaxmin()
	
	#check if already exists

	if file.find('objects') is None:
		objcategory = ET.SubElement(file,'objects')
	#not really sure how to index with elementtree. For example, after checking objname, which
	#was proven to exist, the iterator can't find it the second them. Essentially, adding it to the 
	#tree didn't allow it to be detected :v

	objcategory = file.find('objects')
	assert not objcategory is None, "Not valid"

	
	string = "./objects/" + str(objname)
	if file.find('objects').find(str(objname)) is None:
		obj = ET.SubElement(objcategory, objname, {'directory':source})

	#directory, x,y are all attrib, not subelements.
	"""
	if objname not in file['object'].keys():
		file['object'][objname] = {}
	if 'directory' not in file['object'][objname].keys(): 
		file['object'][objname]['directory'] = {source}
	"""

	#The goal is to derive all children. Trouble is grandchildren indexing is quite confusing.
	#No decent tutorial on the web, this is hindering.
	n_bndname = len(list(file.find('objects').find(str(objname)).iter()  ))
	bndname = 'bndbox_' + str(n_bndname-1)
		#no need to assert bndbox, its number is already based on their lengths.
	
	attrib = {
		'xmin':str(xmin),
		'ymin':str(ymin),
		'xmax':str(xmax),
		'ymax':str(ymax),
		'class':str(currentClass)
	}
	obj = file.find(string)
	bndbox = ET.SubElement(obj,bndname,attrib)


		

def mousecropping(event, x, y, flags, param):
	global refPt, cropping, status,currentImg, currentImgRAM, refPti
	
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
		refPti=(x,y)
		
		

	elif event == cv2.EVENT_MOUSEMOVE:
		if cropping == True:
			status = "1st corner: {}, 2nd corner: {}, time: {}".format(refPti,(x,y),datetime.datetime.now())
			currentImgRAM = currentImg
			currentImgRAM = cv2.rectangle(currentImgRAM,refPti,(x,y),(0,255,0),2)


	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x, y))
		cropping = False
		addbndtoobject()

def StartWindow():

	cv2.namedWindow(windowName, flags=cv2.WINDOW_NORMAL)
	cv2.resizeWindow(windowName,500,500)
	cv2.namedWindow("Info", flags=cv2.WINDOW_GUI_NORMAL)
	cv2.resizeWindow("Info", 500,300)
	cv2.createTrackbar('Class', windowName,0, num_class, nothing)
	

def main():
	parser = arg.ArgumentParser()
	#parser.add_argument("-f", "--folder", required=False, help="Folder to the input, will run lol.jpg on default (better not touch that)")
	#parser.add_argument("-v", "--video", required=False,help="Start with cam mode")
	parser.add_argument("-r", "--reload", required=False,help="Reload imageload.xml")
	args = vars(parser.parse_args())

	#imageloader_importpath()
	mainUI()	
	
	

if __name__ == "__main__":
	main()
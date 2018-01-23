
import numpy as np
import cv2
from copy import deepcopy
from PIL import Image
import pytesseract as tess
from lplate import Main


def preprocess(img):
	#cv2.imshow("Input",img)
	imgBlurred = cv2.GaussianBlur(img, (5,5), 0)
	gray = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)
	sobelx = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=3)
	#cv2.imshow("Sobel",sobelx)
	#cv2.waitKey(0)
	ret2,threshold_img = cv2.threshold(sobelx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#cv2.imshow("Threshold",threshold_img)
	#cv2.waitKey(0)
	return threshold_img

def cleanPlate(plate):
	#print("CLEANING PLATE. . .")
	gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
	#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
	#thresh= cv2.dilate(gray, kernel, iterations=1)
	_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
	im1,contours,hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	if contours:
		areas = [cv2.contourArea(c) for c in contours]
		max_index = np.argmax(areas)
		max_cnt = contours[max_index]
		max_cntArea = areas[max_index]
		x,y,w,h = cv2.boundingRect(max_cnt)
		if not ratioCheck(max_cntArea,w,h):
			return plate,None
		cleaned_final = thresh[y:y+h, x:x+w]
		#cv2.imshow("Function Test",cleaned_final)
		return cleaned_final,[x,y,w,h]
	else:
		return plate,None

def extract_contours(threshold_img):
	element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
	morph_img_threshold = threshold_img.copy()
	cv2.morphologyEx(src=threshold_img, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
	#cv2.imshow("Morphed",morph_img_threshold)
	#cv2.waitKey(0)
	im2,contours, hierarchy= cv2.findContours(morph_img_threshold,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
	return contours

def ratioCheck(area, width, height):
	ratio = float(width) / float(height)
	if ratio < 1:
		ratio = 1 / ratio
	aspect = 4.7272
	min = 15*aspect*15  # minimum area
	max = 125*aspect*125  # maximum area
	rmin = 3
	rmax = 6
	if (area < min or area > max) or (ratio < rmin or ratio > rmax):
		return False
	return True

def isMaxWhite(plate):
	avg = np.mean(plate)
	if(avg>=115):
		return True
	else:
 		return False

def validateRotationAndRatio(rect):
	(x, y), (width, height), rect_angle = rect
	if(width>height):
		angle = -rect_angle
	else:
		angle = 90 + rect_angle
	if angle>15:
	 	return False
	if height == 0 or width == 0:
		return False
	area = height*width
	if not ratioCheck(area,width,height):
		return False
	else:
		return True

def cleanAndRead(img,contours):
	currentlpn=[]
	previouslpn=[]
	currentlpl=[]
	previouslpl=[]
	prevresultlp = []
	prevresultind = []
	i=-1;
	currresultlp = []
	currresultind = []
	j=-1;
	flag=0
	plate=Main.main('image7.jpg')
	text,cordinates=plate
	text=text.strChars
	x,y=cordinates
	print(x,y)
	#count=0
	if (len(text)>7):
	  currentlpn.append(text)
	  currentlpl.append(x)
	  currentlpl.append(y)
	  if(flag!=0):
	    for element in previouslpn:
	      i=i+1
	      if element in currentlpn:
	        prevresultlp.append(element)
	        prevresultind.append(i)
	    for element in currentlpn:
	      j=j+1
	      if element in previouslpn:
	        currresultlp.append(element)
	        currresultind.append(j)
	    distx1=[],distx2=[],disty1=[],disty2=[]
	    for ind in prevresultind:
	      distx1.append(previouslpl[ind*2])
	      disty1.append(previouslpl[(ind*2)+1])
	    for ind in currresultind:
	      distx2.append(currentlpl[ind*2])
	      disty2.append(currentlpl[(ind*2)+1])
	    for ind in distx1:
	      speed=math.sqrt((distx2[ind]-distx1[ind])**2 + (disty2[ind]-disty1[ind])**2)
	      print (speed,"ghhg")
	      if(speed > 10) :
	        update(text)
	    previouslpn=list(currentlpn)
	    previouslpl=list(currentlpl)
	    flag=1
	    del currentlpn[:]
	    del currentlpl[:]
					   

					#img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
					
def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)
def SpeedViolation(file):
	cap = cv2.VideoCapture(file)
	while True :
	     ret, image_np = cap.read()
		#print("DETECTING PLATE . . .")
		#img1 = cv2.imread("testData/Final.JPG")
	     img = image_np
		#print(img1.shape,"dddddddddddddddddddddddddddddd")
		#print(len(img))
		#print(len(img[0]))
	     threshold_img = preprocess(img)
	     contours= extract_contours(threshold_img)
	#if len(contours)!=0:
		#print len(contours) #Test
		# cv2.drawContours(img, contours, -1, (0,255,0), 1)
		# cv2.imshow("Contours",img)
		# cv2.waitKey(0)
	     cleanAndRead(img,contours)
	     cv2.imshow('object detection', cv2.resize(image_np, (800,600)))
	     if cv2.waitKey(25) & 0xFF == ord('q'):
	       cv2.destroyAllWindows()
	       

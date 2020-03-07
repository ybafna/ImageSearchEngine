import numpy as np
import cv2

class ColorDescriptor:
	def __init__(self,bins):
		self.bins = bins

	def histogram(self, image, mask):
		hist = cv2.calcHist([image],[0,1,2],mask,self.bins,[0,180,0,256,0,256])
		hist = cv2.normalize(hist).flatten()
		return hist

		
	def describe(self,image):

		image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
		features = []

		(h, w) = image.shape[:2]

		(cx, cy) = (int(w*0.5),int(h*0.5))

		segments = [(0,cx,0,cy),(cx,w,0,cy),(cx,w,cy,h),(0,cx,cy,h)]

		(axesX, axesY) = (int(w*0.75)/2,int(h*0.75)/2)
		ellipMask = np.zeros(image.shape[:2],dtype = "uint8")
		cv2.ellipse(ellipMask,(cx,cy),(axesX,axesY),0,0,360,255,-1)

		for(startX,endX,startY,endY) in segments:

			cornerMask = np.zeros(image.shape[:2],dtype = "uint8")
			cv2.rectangle(cornerMask,(startX,startY),(endX,endY),255,-1)
			cornerMask = cv2.subtract(cornerMask,ellipMask)


			hist = self.histogram(image, cornerMask)
			features.extend(hist)

		hist = self.histogram(image,ellipMask)
		features.extend(hist)

		return features

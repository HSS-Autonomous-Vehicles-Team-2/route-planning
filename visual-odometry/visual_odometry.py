import numpy as np 
import cv2
import matplotlib.pyplot as plt 
import math 
import time

STAGE_FIRST_FRAME = 0
STAGE_SECOND_FRAME = 1
STAGE_DEFAULT_FRAME = 2
kMinNumFeature = 1500

lk_params = dict(winSize  = (15, 15), 
				maxLevel = 3,
             	criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

def featureTracking(image_ref, image_cur, px_ref):
	kp2, st, err = cv2.calcOpticalFlowPyrLK(image_ref, image_cur, px_ref, None, **lk_params)  #shape: [k,2] [k,1] [k,1]

	st = st.reshape(st.shape[0])
	kp1 = px_ref[st == 1]
	kp2 = kp2[st == 1]

	return kp1, kp2


class PinholeCamera:
	def __init__(self, K=0, D = 0, height =0, width=0):
		self.K = K
		self.D = D
		self.width = width
		self.height = height


class VisualOdometry:
	def __init__(self, cam):
		self.frame_stage = 0
		self.cam = cam
		self.new_frame = None
		self.last_frame = None
		self.cur_R = None
		self.cur_t = None
		self.px_ref = None
		self.px_cur = None
		self.target_px_ref = None
		self.target_frame = None
		self.E = None
		self.focal = cam.K[0][0]
		self.pp = (cam.K[0][2], cam.K[1][2])
		self.trueX, self.trueY, self.trueZ = 0, 0, 0 
		self.detector = cv2.FastFeatureDetector_create(threshold=30, nonmaxSuppression=True)

	def getAbsoluteScale(self, frame_id):  #specialized for KITTI odometry dataset
		ss = self.annotations[frame_id-1].strip().split()
		x_prev = float(ss[3])
		y_prev = float(ss[7])
		z_prev = float(ss[11])
		ss = self.annotations[frame_id].strip().split()
		x = float(ss[3])
		y = float(ss[7])
		z = float(ss[11])
		self.trueX, self.trueY, self.trueZ = x, y, z
		return np.sqrt((x - x_prev)*(x - x_prev) + (y - y_prev)*(y - y_prev) + (z - z_prev)*(z - z_prev))

	def processFirstFrame(self):
		self.px_ref = self.detector.detect(self.new_frame)
		#self.px_ref = self.detector.detectAndCompute(self.new_frame, None)
		img = cv2.drawKeypoints(self.new_frame, self.px_ref, self.new_frame, color=(255,0,0))
		plt.figure(figsize=(12, 8))
		plt.imshow(img)
		plt.axis('off')
		plt.show()
		self.px_ref = np.array([x.pt for x in self.px_ref], dtype=np.float32)
		self.target_px_ref = self.px_ref
		self.target_frame = self.new_frame
		self.frame_stage = STAGE_SECOND_FRAME

	def processSecondFrame(self):
		self.px_ref, self.px_cur = featureTracking(self.target_frame, self.new_frame, self.target_px_ref)
		E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
		_, self.cur_R, self.cur_t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
		self.frame_stage = STAGE_DEFAULT_FRAME 
		self.px_ref = self.px_cur
		self.E = E

	def processFrame(self):
		self.px_ref, self.px_cur = featureTracking(self.target_frame, self.new_frame, self.target_px_ref)
		E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
		_, R, t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
		
		print(R)
		print(t)
		sy = np.sqrt(R[2,1]*R[2,1]+ R[2,2]*R[2,2])
		x = math.atan2(R[2,1] , R[2,2])
		x = math.degrees(x)
		y = math.atan2(-R[2,0], sy)
		y = math.degrees(y)
		z = math.atan2(R[1,0], R[0,0])
		z = math.degrees(z)
		#plt.figure(figsize=(12, 8))
		#plt.axis('off')
		#plt.show()
		#absolute_scale = self.getAbsoluteScale(frame_id)
		#if(absolute_scale > 0.1):
		#	self.cur_t = self.cur_t + absolute_scale*self.cur_R.dot(t) 
		#	self.cur_R = R.dot(self.cur_R)
		if(self.px_ref.shape[0] < kMinNumFeature):
			self.px_cur = self.detector.detect(self.new_frame)
			self.px_cur = np.array([x.pt for x in self.px_cur], dtype=np.float32)
		self.px_ref = self.px_cur
		return x,y,z

	def set_target(self,img):
		assert(img.ndim==2 and img.shape[0]==self.cam.height and img.shape[1]==self.cam.width), "Frame: provided image has not the same size as the camera model or image is not grayscale"
		self.new_frame = img
		self.processFirstFrame()


	def update(self, img):
		assert(img.ndim==2 and img.shape[0]==self.cam.height and img.shape[1]==self.cam.width), "Frame: provided image has not the same size as the camera model or image is not grayscale"
		self.new_frame = img
		x = 0
		y = 0
		z = 0
		if(self.frame_stage == STAGE_DEFAULT_FRAME):
			print("default Frame")
			x,y,z = self.processFrame()
		elif(self.frame_stage == STAGE_SECOND_FRAME):
			print("Second Frame")
			self.processSecondFrame()
		elif(self.frame_stage == STAGE_FIRST_FRAME):
			self.processFirstFrame(img)
		self.last_frame = self.new_frame
		return x,y,z

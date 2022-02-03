from cv2 import drawChessboardCorners
import numpy as np
import cv2
import glob


sideB = 8
sideA = 6


endCriteria = (cv2.TermCriteria_EPS+cv2.TermCriteria_MAX_ITER, 30, 0.001)

objp = np.zeros((sideA*sideB,3),np.float32)
objp[:,:2] = np.mgrid[0:sideA,0:sideB].T.reshape(-1,2)


objecPoints = []
imagePoints = []


calibrationImages = glob.glob("calibrationImages_640_480/*.jpg")

print(f"Found {len(calibrationImages)} images")


for fname in calibrationImages:
    calImage = cv2.imread(fname)
    grayImage = cv2.cvtColor(calImage,cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(grayImage, (sideA,sideB),None)
    print(f"image {fname} chess board was {ret}")
    if ret == True:
        objecPoints.append(objp)

        corners2 = cv2.cornerSubPix(grayImage,corners,(11,11),(-1,-1),endCriteria)
        imagePoints.append(corners)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objecPoints,imagePoints,grayImage.shape[::-1],None,None) 

height, width = calImage.shape[:2]
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(mtx,dist, (width,height),1,(width,height))

mapx, mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newCameraMatrix,(width, height),5)
dst = cv2.remap(calImage,mapx,mapy,cv2.INTER_LINEAR)

x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite("test222.png", dst)

np.save("camereaMatrix",mtx)
np.save("distortionCoefficent",dist)
np.save("newCamereaMatrix",newCameraMatrix)
np.save("roi",roi)
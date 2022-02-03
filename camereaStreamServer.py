import io
import socket
import struct
import cv2
import numpy as np
import time

import threading

from dt_apriltags import Detector

frameData = 0

#TODO split into functions and helper functions
def cameraStreamGet(HOST,PORT):
    global frameData
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    try:
        while True:
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            image_stream.seek(0)
            byteRaw = np.asarray(bytearray(image_stream.read()),dtype=np.uint8)
            frameData = cv2.imdecode(byteRaw,cv2.IMREAD_ANYCOLOR)
    finally:
        connection.close()
        server_socket.close()

def saveImage(frame):
    nameForimage = str(time.time())+".jpg"
    print(f"Saving Calibration: {nameForimage}")
    cv2.imwrite(nameForimage,frame)
    time.sleep(3)

def drawApriltag(frame, detector):
    grayImage = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    tagsFound = detector.detect(grayImage)

    for tag in tagsFound:
        for idx in range(len(tag.corners)):
            cv2.line(frame, tuple(tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

        cv2.putText(frame, str(tag.tag_id),
                    org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8,
                    color=(0, 0, 255))
        cv2.putText(frame, (str(int(tag.center[0]))+","+str(int(tag.center[1]))),
                    org=(tag.corners[0, 0].astype(int)-50,tag.corners[0, 1].astype(int)-50),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8,
                    color=(255, 0, 255))
    
    return frame

KEYQ = 81
KEYq = 113

KEYC = 67
KEYc = 99

KEYR = 82
KEYr = 114

KEYA = 65
KEYa = 97

serverIP = "***.***.***.***" 
portNum = 8000

frameGraber = threading.Thread(target=cameraStreamGet, args=(serverIP,portNum),daemon=True)

screenName = "Test Frames"
cv2.namedWindow(screenName,cv2.WINDOW_NORMAL)

mtx = np.load("cameraCalibrations/camereaMatrix.npy")
dist = np.load("cameraCalibrations/distortionCoefficent.npy")
newMtx = np.load("cameraCalibrations/newCamereaMatrix.npy")
roi = np.load("cameraCalibrations/roi.npy")

frameGraber.start()

objectPoints = [[9.0,6.4,0.0],[9.0,41.3,0.0],[49.6,6.4,0.0],[49.6,41.3,0.0]]
pixelpoints = [[454,75],[146,65],[431,338],[77,335]]

_, rvec, tvec = cv2.solvePnP(objectPoints,pixelpoints,mtx,dist)



aprilDetector = Detector("tag36h11",1,1.0,0.0,1,0.25,0) #Useses default detection

runRemap = False
runAprilTag = False

while True:
    if runRemap == True:
        height, width = frameData.shape[:2]
        mapx, mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newMtx,(width, height),5)
        dst = cv2.remap(frameData,mapx,mapy,cv2.INTER_LINEAR)

        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
    elif runRemap == False:
        dst = frameData
    if runAprilTag == True:
        dst = drawApriltag(dst,aprilDetector)
    
    if cv2.waitKey(1) == KEYQ or cv2.waitKey(1) == KEYq:
        print("Ending")
        break
    elif cv2.waitKey(1) == KEYC or cv2.waitKey(1) == KEYc:
        saveImage(frameData)
    elif cv2.waitKey(1) == KEYR or cv2.waitKey(1) == KEYr:
        if runRemap == True:
            runRemap = False
        elif runRemap == False:
            runRemap = True
        print(f"Remaping is now: {runRemap}")
    elif cv2.waitKey(1) == KEYA or cv2.waitKey(1) == KEYa:
        if runAprilTag == True:
            runAprilTag = False
        elif runAprilTag == False:
            runAprilTag = True
        print(f"Apriltag is now: {runAprilTag}")
    
    cv2.imshow(screenName,dst)

print("Test end camera")

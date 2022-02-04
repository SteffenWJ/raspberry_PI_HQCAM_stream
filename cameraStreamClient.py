import io
import socket
import struct
import time
import picamera

#Fra https://picamera.readthedocs.io/en/release-1.13/recipes2.html#rapid-capture-and-streaming


serverIP = '***.***.***.***' 
portNum = **** 


client_socket = socket.socket()
client_socket.connect((serverIP, portNum)) #Tuple becaus of how IP4 handles it's connection
connection = client_socket.makefile('wb')


try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        #camera.resolution = (1280, 720)
        camera.framerate = 30
        #camera.awb_mode = "auto"
        time.sleep(2)
        start = time.time()
        count = 0
        stream = io.BytesIO()
        # Use the video-port for captures...
        for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            count += 1
            #if time.time() - start > 10:
            #q    break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
    finish = time.time()
print('Sent %d images in %d seconds at %.2ffps' % (
    count, finish-start, count / (finish-start)))

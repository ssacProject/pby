
gst_str = ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)480, height=(int)360, format=(string)NV12, framerate=(fraction)60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)480, height=(int)360, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
#gst_str = ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)640, height=(int)480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

import cv2
import numpy as np
import lane_detection
import time
from OpenCV_Functions import *
import motorDef

def Video(openpath):
    cap = cv2.VideoCapture(openpath)
    time.sleep(2)
    if cap.isOpened():
        print("Video Opened")
    else:
        print("Video Not Opened")
        print("Program Abort")
        exit()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    #fourcc = cv2.VideoWriter_fourcc('m','p','4','v') with *.mp4 save

    cv2.namedWindow("Input", cv2.WINDOW_GUI_EXPANDED)

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        #frame = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_AREA)
        if ret:
            #height, width = frame.shape[:2]
            #line_horizontal_start, line_horizontal_end = (int(width* 0.45), int(height*0.6)), (int(width * 0.55), int(height * 0.6))
            #linecv = cv2.line(frame, line_horizontal_start, line_horizontal_end, (255,0,0),3)
            #lane_detect = hough(frame)
            #cv2.imshow("input", lane_detect)
#            lane_detect = lane_detection.LaneDetectImg(frame)
                #lane_detect = lane_detection.hough(frame)
            #cv2.imshow("input", lane_detect)
            
            try:
                #canny
                #canny_edge = lane_detection.LaneDetectImg_canny(frame)
                #cv2.imshow("canny", canny_edge)
                
                lane_detect = lane_detection.LaneDetectImg(frame)
                cv2.imshow("input", lane_detect)
                #cv2.waitKey(0)
            except:
                frame = lane_detection.centerAim(frame)
                cv2.imshow("input", frame)
            #lane_detect = lineFitting(frame)
            # Display the resulting frame
            #cv2.imshow("Input", lane_detect)
            #cv2.imshow("test", linecv)

        else:
            break
        # waitKey(int(1000.0/fps)) for matching fps of video
        if cv2.waitKey(int(1000.0/fps)) & 0xFF == ord('q'):
            motorDef.all_stop() #motor stop
            break
    # When everything done, release the capture
    cap.release()

    cv2.destroyAllWindows()
    return
   
if __name__=="__main__":
    #motorDef.motor_init()
    Video(gst_str)

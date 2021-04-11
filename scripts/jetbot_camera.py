
gst_str = ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)480, height=(int)360, format=(string)NV12, framerate=(fraction)60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)480, height=(int)360, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
#gst_str = ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)640, height=(int)480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
#480 360
import cv2
import numpy as np
import lane_detection
import time
from OpenCV_Utils import *
import motorDef

def Video(): #openpath
    openpath = gst_str
    cap = cv2.VideoCapture(openpath)
    time.sleep(2)
    if cap.isOpened():
        print("Video Opened")
    else:
        print("Video Not Opened")
        print("Program Abort")
        exit()
    fps = 60    
    #fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    #fourcc = cv2.VideoWriter_fourcc('m','p','4','v') with *.mp4 save

    cv2.namedWindow("Input", cv2.WINDOW_GUI_EXPANDED)

    while cap.isOpened():
        # Capture frame-by-frame
#        start_time = time.time()
        ret, frame = cap.read()
        #frame = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_AREA)
        if ret:
#            lane_detect = lane_detection.LaneDetectImg(frame)
            
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
#        end_time2 = time.time()
#        print("time1 :", end_time2 - start_time)
        
        if cv2.waitKey(int(1000.0/fps)) & 0xFF == ord('q'):
            motorDef.real_stop() #motor stop
            break
#        end_time = time.time()
#        print("delay :", end_time - start_time)
    # When everything done, release the capture
    cap.release()

    cv2.destroyAllWindows()
    return
   
if __name__=="__main__":
    #Video(gst_str)
    Video()

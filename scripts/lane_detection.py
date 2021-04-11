from OpenCV_Utils import *
import motorDef
import yellow_Filter as ft
g_state = 0
def LaneDetectImg(imagePath):
    #image = cv2.imread(imagePath) 
    image = imagePath
    #imageShow("image", image)
    
    #image_gray = convertColor(image, cv2.COLOR_BGR2GRAY)
    g_blur = ft.gaussian_blur(image, 9)
    y_filter = ft.hsvscale(g_blur)
    image_edge = cannyEdge(y_filter, 100, 200)
#    cv2.imshow("hsv", y_filter)
#    cv2.imshow("canny", image_edge)
    height, width = image.shape[:2]
    pt1 = (width*0.35, height*0.5) # up left 0.25 0.6 height 0.6
    pt2 = (width*0.65, height*0.5) # up right 0.85 0.6
    pt3 = (width*0.8, height*0.8) # under right 0.85 1.0 height 1.0
    pt4 = (width*0.2, height*0.8) # under left 0.25 1.0
    
    #cpt = (int(width*0.5), int(height*0.6)) 
    cpt = cptF(image)

    roi_corners = np.array([[pt1, pt2, pt3, pt4]], dtype=np.int32)
    
    image_roi = polyROI(image_edge, roi_corners)

    #lines = houghLinesP(image_roi, 1, np.pi/180, 40, 40, 15) #ok
    #lines = houghLinesP(image_roi, 1, np.pi/180, 40, 40, 25)
    
    lines = houghLinesP(image_roi, 1, np.pi/180, 40, 40, 20)
    #drawhough = drawHoughLinesP(image, lines)
    #cv2.imshow("hough", drawhough) 
    #print("lines", lines)
    
    centerPt = centerPoints(image_roi, lines, (0, 0, 255), 2) #center Point2 for distance
    if centerPt == 1 :
        motorDef.all_stop(g_state)
        print("centerPoints is None")
    #print("centerPt", centerPt)
    '''
    #centerPt0 = np.array([centerPt])
    #print(centerPt0)
    #drawhough = drawHoughLinesP(image, centerPt0)
    #cv2.imshow("centerhough", drawhough) 
    '''
    #

    image_lane = centerLineFitting(image, lines, (0, 0, 255), 2) #image , draw image + lines


    if centerPt == -1: 
        print("point of center Line not exist")
    else:
        centerPt_min = [centerPt[0][0], centerPt[0][1]]
        centerPt_max = [centerPt[1][0], centerPt[1][1]]
    
        ptLen = dist(cpt, centerPt_min, centerPt_max)

        distance = distSign(cpt, centerPt_min, centerPt_max, ptLen)
        #print("distance")
        distance = round(distance, 2)
        print(distance, "\n")
        
        g_state = motorDef.motor_run(distance, 0)

        if distance is None:
            print("distance is none all_stop")
            motorDef.all_stop(g_state)

        #print("motor OK")
        
    image_lane = centerAim(image_lane)
    
    return image_lane


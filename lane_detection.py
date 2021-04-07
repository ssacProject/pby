from OpenCV_Utils import *
import motorDef

def LaneDetectImg(imagePath):
    #image = cv2.imread(imagePath) 
    image = imagePath

    #imageShow("image", image)
    
    image_gray = convertColor(image, cv2.COLOR_BGR2GRAY)
    image_edge = cannyEdge(image_gray, 100, 200)
    height, width = image.shape[:2]
    pt1 = (width*0.0, height*0.6) # up left 0.25 0.6
    pt2 = (width*1.0, height*0.6) # up right 0.85 0.6
    pt3 = (width*0.0, height*1.0) # under right 0.85 1.0
    pt4 = (width*1.0, height*1.0) # under left 0.25 1.0
    
    #cpt = (int(width*0.5), int(height*0.5)) 
    cpt = cptF(image)

    roi_corners = np.array([[pt1, pt2, pt3, pt4]], dtype=np.int32)
    
    image_roi = polyROI(image_edge, roi_corners)
    #imageShow("image_roi", image_roi) #cannyedge check
    
    #''' #canny_edge
    #lines = houghLinesP(image_roi, 1, np.pi/180, 40, 70, 15)
    #print("lines", lines)
    lines = houghLinesP(image_roi, 1, np.pi/180, 40, 40, 15)

#    hough_image = drawHoughLinesP(image, lines) # draw houghLinesP
    
    #'''
    #print("houghLinesP", lines) #line check
    #image_lane = lineFitting(image, lines, (0, 0, 255), 3, 5. * np.pi / 180.)
    #centerPt = centerPoints(image, lines, (0, 0, 255), 2)
    
    centerPt = centerPoints(image, lines, (0, 0, 255), 2)
    if centerPt == 1 :
        motorDef.all_stop()
        print("centerPoints is None")
    #try:
        #centerPt = centerPoints(image, lines, (0, 0, 255), 2)
    image_lane = centerLineFitting(image, lines, (0, 0, 255), 2)
    # except:
    #     if image_lane == 1:
    #         print("all_stop()")
    #         motorDef.all_stop()
    #         print("image_lane")
    #         return 1

    if centerPt == -1: 
        print("point of center Line not exist")
    else:
        centerPt_min = [centerPt[0][0], centerPt[0][1]]
        centerPt_max = [centerPt[1][0], centerPt[1][1]]
    
        #midLinePoint = centerLinePts_point(lines, cpt)
    
        ptLen = dist(cpt, centerPt_min, centerPt_max)

        distance = distSign(cpt, centerPt_min, centerPt_max, ptLen)
        print("distance")
        print(distance, "\n")

        if motorDef.motor_run(distance) == -1:
            print("distance is none all_stop")
            motorDef.all_stop()
        print("motor OK")
    
    image_lane = centerAim(image_lane)
    
    #'''
    #''' #canny_edge
    #return image_roi #canny_edge
    #return hough_image 
    return image_lane


def LaneDetectImg_canny(imagePath):
    #image = cv2.imread(imagePath) 
    image = imagePath

    #imageShow("image", image)
    
    image_gray = convertColor(image, cv2.COLOR_BGR2GRAY)
    image_edge = cannyEdge(image_gray, 100, 200)
    height, width = image.shape[:2]
    pt1 = (width*0.35, height*0.6)
    pt2 = (width*0.65, height*0.6)
    pt3 = (width*0.85, height*1.0)
    pt4 = (width*0.25, height*1.0)
    
    #cpt = (int(width*0.5), int(height*0.5)) 
    cpt = cptF(image)

    roi_corners = np.array([[pt1, pt2, pt3, pt4]], dtype=np.int32)
    
    
    image_roi = polyROI(image_edge, roi_corners)
    #imageShow("image_roi", image_roi) #cannyedge check
    
    #''' #canny_edge
    #lines = houghLinesP(image_roi, 1, np.pi/180, 40, 70, 15)
    #print("lines", lines)
    
    #hough_image = drawHoughLinesP(image, lines) # draw houghLinesP
    
    '''
    #print("houghLinesP", lines) #line check
    #image_lane = lineFitting(image, lines, (0, 0, 255), 3, 5. * np.pi / 180.)
    centerPt = centerPoints(image, lines, (0, 0, 255), 2, 5. * np.pi / 180.)
    image_lane = centerLineFitting(image, lines, (0, 0, 255), 2, 5. *  np.pi / 180.)
    #image_lane = lineFittingOneSide(image, lines, (0, 0, 255), 2, np.pi / 180.)

    centerPt_min = [centerPt[0][0], centerPt[0][1]]
    centerPt_max = [centerPt[1][0], centerPt[1][1]]
    
    ptLen = dist(cpt, centerPt_min, centerPt_max)
    print("distance")
    print(ptLen)
    
    image_lane = centerAim(image_lane)
    
    
    #image_line = cv2.line(image_lane, pt1i, pt4i, (0, 255, 0), 5)
    #image_line = cv2.line(image_lane, pt2i, pt3i, (0, 255, 0), 5)
    '''
    #''' #canny_edge
    return image_roi #canny_edge
    #return hough_image 
    #return image_lane


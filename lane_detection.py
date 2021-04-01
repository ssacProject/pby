from OpenCV_Functions import *

'''
def splitTwoSideLines(lines, slope_threshold = (5. * np.pi / 180.)):
    lefts = []
    rights = []
    for line in lines:
        x1 = line[0,0]
        y1 = line[0,1]
        x2 = line[0,2]
        y2 = line[0,3]
        if (x2-x1) == 0:
            continue
        slope = (float)(y2-y1)/(float)(x2-x1)
        if abs(slope) < slope_threshold:
            continue
        if slope <= 0:
            lefts.append([slope, x1, y1, x2, y2])
        else:
            rights.append([slope, x1, y1, x2, y2])
    return lefts, rights
def medianPoint(x):
    if len(x) == 0:
        return None
    else:
        xx = sorted(x)
        return xx[(int)(len(xx)/2)]
def interpolate(x1, y1, x2, y2, y):
    return int(float(y - y1) * float(x2-x1) / float(y2-y1) + x1)
def lineFitting(image, lines, color = (0,0,255), thickness = 3, slope_threshold = (5. * np.pi / 180.)):
    result = imageCopy(image)
    height = image.shape[0]
    lefts, rights = splitTwoSideLines(lines, slope_threshold)
    left = medianPoint(lefts)
    right = medianPoint(rights)
    min_y = int(height*0.6)
    max_y = height
    min_x_left = interpolate(left[1], left[2], left[3], left[4], min_y)
    max_x_left = interpolate(left[1], left[2], left[3], left[4], max_y)
    min_x_right = interpolate(right[1], right[2], right[3], right[4], min_y)
    max_x_right = interpolate(right[1], right[2], right[3], right[4], max_y)
    cv2.line(result, (min_x_left, min_y), (max_x_left, max_y), color, thickness)
    cv2.line(result, (min_x_right, min_y), (max_x_right, max_y), color, thickness)
    return result
'''
def dist(P, A, B):
    area = abs ( (A[0] - P[0]) * (B[1] - P[1]) - (A[1] - P[1]) * (B[0] - P[0]) )
    AB = ( (A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 ) ** 0.5
    return ( area / AB )

def LaneDetectImg(imagePath):
    #image = cv2.imread(imagePath) 
    image = imagePath

    #imageShow("image", image)
    
    image_gray = convertColor(image, cv2.COLOR_BGR2GRAY)
    image_edge = cannyEdge(image_gray, 100, 200)
    height, width = image.shape[:2]
    pt1 = (width*0.45, height*0.35)
    pt2 = (width*0.65, height*0.35)
    pt3 = (width*0.8, height*1.0)
    pt4 = (width*0.2, height*1.0)
    
    cpt = (int(width*0.5), int(height*0.5)) 
    
    #pt1i = (int(width*0.45), int(height*0.35))
    #pt2i = (int(width*0.55), int(height*0.35))
    #pt3i = (int(width*0.8), int(height*1.0))
    #pt4i = (int(width*0.2), int(height*1.0))
    
    #image_edge1 = image_edge
    #image_edge1 = cv2.line(image_edge1, pt1i, pt4i, (255, 255, 255), 5)
    #print(image_edge1)
    #image_edge1 = cv2.line(image_edge1, pt2i, pt3i, (255, 255, 255), 5)
    #imageShow("image_edge1", image_edge)
    
    
    line_horizontal_start = ( int(width * 0.45), int(height *0.6))
    line_horizontal_end = (int(width * 0.55), int(height *0.6))
    line_vertical_height = ( int(width * 0.5), int(height *0.55))
    line_vertical_width = (int(width * 0.5), int(height *0.65))
    
    roi_corners = np.array([[pt1, pt2, pt3, pt4]], dtype=np.int32)
    
    image_roi = polyROI(image_edge, roi_corners)
    #imageShow("image_roi", image_roi)
    
    
    lines = houghLinesP(image_roi, 1, np.pi/180, 40)
    #print(lines)
    #image_lane = lineFitting(image, lines, (0, 0, 255), 3, 5. * np.pi / 180.)
    centerPt = centerPoints(image, lines, (0, 0, 255), 2, 5. * np.pi / 180.)
    image_lane = centerLineFitting(image, lines, (0, 0, 255), 2, 5. * np.pi / 180.)
    
    centerPt_min = [centerPt[0][0], centerPt[0][1]]
    centerPt_max = [centerPt[1][0], centerPt[1][1]]
    
    ptLen = dist(cpt, centerPt_min, centerPt_max)
    print("distance")
    print(ptLen)
    
    #image_lane2 = centerLine(image, lines, (0, 0, 255), 3, 5. * np.pi / 180.)
    image_lane = cv2.line(image_lane, line_horizontal_start, line_horizontal_end, (255, 0, 0), 3)
    image_lane = cv2.line(image_lane, line_vertical_height, line_vertical_width, (255, 0, 0), 3)
    
    
    #image_line = cv2.line(image_lane, pt1i, pt4i, (0, 255, 0), 5)
    #image_line = cv2.line(image_lane, pt2i, pt3i, (0, 255, 0), 5)
    
    return image_lane
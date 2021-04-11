import cv2
import numpy as np
import math 

def imageCopy(src):
    return np.copy(src)

def CutRectROI(image, x1, y1, x2, y2):
    return image[y1:y2, x1:x2]

def PasteRectROI(image, x1, y1, dst):
    y2, x2 = image.shape[:2]
    dst[y1:y1+y2, x1:x1+x2]=image
    return dst

def makeBlackImage(image, color=False):
    height, width = image.shape[0], image.shape[1]
    if color is True:
        return np.zeros((height, width, 3), np.uint8)
    else:
        if len(image.shape) == 2:
            return np.zeros((height, width), np.uint8)
        else:
            return np.zeros((height, width, 3), np.uint8)

def fillPolyROI(image, points):
    if len(image.shape) == 2:
        channels = 1
    else:
        channels = image.shape[2]
    mask = makeBlackImage(image)
    ignore_mask_color = (255,) * channels
    cv2.fillPoly(mask, points, ignore_mask_color)
    return mask

def polyROI(image, points):
    mask = fillPolyROI(image, points)
    return cv2.bitwise_and(image, mask)

def convertColor(image, flag=cv2.COLOR_BGR2GRAY):
    return cv2.cvtColor(image, flag)

def splitImage(image):
    return cv2.split(image)

def mergeImage(channel1, channel2, channel3):
    return cv2.merge((channel1, channel2, channel3))

def rangeColor(image, lower, upper):
    result = imageCopy(image)
    return cv2.inRange(result, lower, upper)

def splitColor(image, lower, upper):
    result = imageCopy(image)
    mask = rangeColor(result, lower, upper)
    return cv2.bitwise_and(result, result, mask=mask)

def drawLine(image, point1, point2, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_AA):
    result = imageCopy(image)
    return cv2.line(result, point1, point2, color, thickness, lineType)

def drawRect(image, point1, point2, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_AA):
    result = imageCopy(image)
    return cv2.rectangle(result, point1, point2, color, thickness, lineType)    

def drawText(image, text, point=(10, 10), font=cv2.FONT_HERSHEY_PLAIN, fontScale=2.0, color=(255,255,255), thickness=3, lineType=cv2.LINE_AA):
    result = imageCopy(image)
    return cv2.putText(result, text, point, font, fontScale, color, thickness, lineType)
    
def addImage(image1, image2):
    return cv2.add(image1, image2)

def imageThreshold(image, thresh=128, maxval=255, type=cv2.THRESH_BINARY):
    _, res = cv2.threshold(image, thresh=thresh, maxval=maxval, type=type)
    return res

def cannyEdge(image, threshold1=100, threshold2=200):
    return cv2.Canny(image, threshold1, threshold2) 

def houghLines(image, rho=1, theta=np.pi/180, threshold=100):
    return cv2.HoughLines(image, rho, theta, threshold)

def houghLinesP(image, rho=1.0, theta=np.pi/180, threshold=100, minLineLength=10, maxLineGap=100):
    return cv2.HoughLinesP(image, rho, theta, threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)

def drawHoughLinesP(image, lines):
    result = imageCopy(image)
    if len(image.shape) == 2:
        result = convertColor(image, cv2.COLOR_GRAY2BGR)
    for i in range(len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 3)
    return result
####################################################


def medianPoint(x):
    if len(x) == 0:
        return None
    else:
        xx = sorted(x)
        return xx[(int)(len(xx)/2)]


def interpolate(x1, y1, x2, y2, y):
    return int(float(y - y1) * float(x2-x1) / float(y2-y1) + x1)

#center line 
def centerLineFitting(image, lines, color = (0,0,255), thickness = 3):
    result = imageCopy(image)
    height = image.shape[0]
    #lefts, rights = splitTwoSideLines(lines, slope_threshold)

    cpt = cptF(image)

    try:
        centers = centerLinePts(lines, cpt) # center point2 return
    except:
        print("centers", centers)
    
    if centers is None:
        print("centers is None")
        return 1 
    center = medianPoint(centers) 

    min_y = int(height*0.4)
    max_y = height

    if center is not None:
        min_x_center = interpolate(center[1], center[2], center[3], center[4], min_y)
        max_x_center = interpolate(center[1], center[2], center[3], center[4], max_y)
        cv2.line(result, (min_x_center, min_y), (max_x_center, max_y), color, thickness)

    return result

def cptF(image):
    height, width = image.shape[:2]
    cpt = (int(width*0.5), int(height*0.4))
    return cpt

def centerLinePts(lines, cpt):
    lefts = []
    rights = []
    centers = []
    all_lines = []
    n = 0
    #print("lines\n", lines)
    #cpt (width, height)
    if lines is None:
        print("lines is None\n")
        return 1
    for line in lines:
        x1 = line[0,0]
        y1 = line[0,1]
        x2 = line[0,2]
        y2 = line[0,3]
        if (x2-x1) == 0:
            x2 = x2 + 1

        slope_degree = (math.atan2(float(y2-y1), float(x2-x1)) * 180) / math.pi
        
        if abs(slope_degree) > 150.0 or abs(slope_degree) < 30.0:
            #print("slope_degree", n+1)
            continue

        all_lines.append([slope_degree, x1, y1, x2, y2])

    inter_list = []
    count = 0
    for i in all_lines:

        inter_x = interpolate(all_lines[count][1], all_lines[count][2], all_lines[count][3], all_lines[count][4], cpt[1])
        count = count + 1

        inter_list.append(inter_x)

    lefts.append(all_lines[inter_list.index(min(inter_list))])
    rights.append(all_lines[inter_list.index(max(inter_list))])

    if lefts is not None:
        if lefts[0][2] > lefts[0][4]:
            lefts[0][1], lefts[0][2], lefts[0][3], lefts[0][4] = lefts[0][3], lefts[0][4], lefts[0][1], lefts[0][2]
    else:
        print("lefts is None\n\n\n\n")
    
    if rights is not None:
        if rights[0][2] > rights[0][4]:
            rights[0][1], rights[0][2], rights[0][3], rights[0][4] = rights[0][3], rights[0][4], rights[0][1], rights[0][2]
    else:
        print("rights is None\n\n\n\n")

    cx1 = (lefts[0][1] + rights[0][1]) / 2
    cy1 = (lefts[0][2] + rights[0][2]) / 2
    cx2 = (lefts[0][3] + rights[0][3]) / 2
    cy2 = (lefts[0][4] + rights[0][4]) / 2

    if (float)(cx2-cx1) == 0:
        cSlope = 0
    else:
        cSlope = (float)(cy2-cy1)/(float)(cx2-cx1)
        centers.append([cSlope, cx1, cy1, cx2, cy2])
    return centers

def centerPoints(image, lines, color = (0,0,255), thickness = 3):
    result = imageCopy(image)
    height = image.shape[0]
    ctp = []            # point of center Red Line
    cpt = cptF(image)  # point of aim
    
    centers = centerLinePts_point(lines, cpt) # center Point2 return
    if centers == 1:
        return 1  

    center = medianPoint(centers) 

    min_y = int(height*0.6)
    max_y = height

    if center is not None:
        min_x_center = interpolate(center[1], center[2], center[3], center[4], min_y)
        max_x_center = interpolate(center[1], center[2], center[3], center[4], max_y)
        cv2.line(result, (min_x_center, min_y), (max_x_center, max_y), color, thickness)
        ctp.append([min_x_center, min_y])
        ctp.append([max_x_center, max_y])
    else:
        print("Open_Util, centerPoints, center is None!! \n")
        return -1
 
    return ctp

def centerLinePts_point(lines, cpt):
    lefts = []
    rights = []
    centers = []
    all_lines = []

    if lines is None:
        print("lines is None\n")
        return 1 
    for line in lines:
        x1 = line[0,0]
        y1 = line[0,1]
        x2 = line[0,2]
        y2 = line[0,3]
        if (x2-x1) == 0:
            x2 = x2 + 1

        slope = (float)(y2-y1)/(float)(x2-x1)
        
        slope_degree = (math.atan2(float(y2-y1), float(x2-x1)) * 180) / math.pi

        if abs(slope_degree) > 150.0 or abs(slope_degree) < 30.0:
            print("slope_degree", n+1)
            continue

        all_lines.append([0, x1, y1, x2, y2])
        
    inter_list = []
    count = 0
    for i in all_lines:
        inter_x = interpolate(all_lines[count][1], all_lines[count][2], all_lines[count][3], all_lines[count][4], cpt[1])
        count = count + 1

        inter_list.append(inter_x)

    lefts.append(all_lines[inter_list.index(min(inter_list))])
    rights.append(all_lines[inter_list.index(max(inter_list))])
            
    if lefts is not None:
        if lefts[0][2] > lefts[0][4]:
            lefts[0][1], lefts[0][2], lefts[0][3], lefts[0][4] = lefts[0][3], lefts[0][4], lefts[0][1], lefts[0][2]
    else:
        print("lefts is None\n\n\n\n")
    
    if rights is not None:
        if rights[0][2] > rights[0][4]:
            rights[0][1], rights[0][2], rights[0][3], rights[0][4] = rights[0][3], rights[0][4], rights[0][1], rights[0][2]
    else:
        print("rights is None\n\n\n\n")
        
    cx1 = (lefts[0][1] + rights[0][1]) / 2
    cy1 = (lefts[0][2] + rights[0][2]) / 2
    cx2 = (lefts[0][3] + rights[0][3]) / 2
    cy2 = (lefts[0][4] + rights[0][4]) / 2

    if (float)(cx2-cx1) == 0:
        cSlope = 0
    else:
        cSlope = (float)(cy2-cy1)/(float)(cx2-cx1)
        centers.append([cSlope, cx1, cy1, cx2, cy2])
    return centers

def dist(P, A, B):
    area = abs ( (A[0] - P[0]) * (B[1] - P[1]) - (A[1] - P[1]) * (B[0] - P[0]) )
    AB = ( (A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 ) ** 0.5
    return ( area / AB )

def distSign(cpt, center_min, center_max, ptLen):
    interpolate_x = interpolate(center_min[0], center_min[1], center_max[0], center_max[1], cpt[1])

    if interpolate_x < cpt[0]:
        ptLen = -ptLen

    return ptLen

def centerAim(image):
    height, width = image.shape[:2]
    line_horizontal_start = ( int(width * 0.45), int(height *0.4))
    line_horizontal_end = (int(width * 0.55), int(height *0.4))
    line_vertical_start = ( int(width * 0.5), int(height *0.35))
    line_vertical_end = (int(width * 0.5), int(height *0.45))

    image_Aim = cv2.line(image, line_horizontal_start, line_horizontal_end, (255, 0, 0), 3)
    image_Aim = cv2.line(image, line_vertical_start, line_vertical_end, (255, 0, 0), 3)
    return image_Aim

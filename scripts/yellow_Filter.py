import cv2

def grayscale(img): # 흑백이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def hsvscale(frame): # image
    lower_yellow = (20,130,130)# 20,100,100
    upper_yellow = (40,255,255)
	
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#    cv2.imshow("hsbaaaa", hsv)
    mask_yellow = cv2.inRange(hsv,lower_yellow,upper_yellow)
    img_result_yellow =cv2.bitwise_and(frame,frame,mask=mask_yellow)
		
    return img_result_yellow

def gaussian_blur(img, kernel_size): # 가우시안 필터
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

  
''' 
  #mian line
  gussian_img = gaussian_blur(image,9)
  yellow_i = hsvscale(gussian_img)
  gray_img = grayscale(yellow_i)
  blur_img = gaussian_blur(gray_img, 3)
  canny_img = canny(blur_img, 80, 210)
'''


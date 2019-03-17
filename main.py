import cv2
import numpy as np
from selenium import webdriver
import winsound

driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com/')

name = input("Enter receiver's name: ")
msg = input("Message to send: ")
input("Enter after you scan QR")

user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
user.click()
# Time you see it, the class may be changed. Should be checked.
msg_box = driver.find_element_by_class_name('_2S1VP')

# Video source
capture = cv2.VideoCapture(0)

bg_sub = cv2.createBackgroundSubtractorMOG2(400, 100, True)
frameCount = 0

while True:
    ret, frame = capture.read()

    if not ret:
        break
    
    frameCount += 1

    # Frame width and height can be resized by fx and fy..
    resizedFrame = cv2.resize(frame, (0, 0), fx=0.7, fy=0.7)

    #foreground mask
    fg_mask = bg_sub.apply(resizedFrame)

    count = np.count_nonzero(fgmask)

    print(f'Frame: {frameCount}, Pixel count: {count}')

    # Count should be adjusted based on your goal.
    if (frameCount > 1 and count > 3000):
        print("SOMEONE IS THERE")
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_35EW6')
        button.click()
        # winsound.Beep() # CAN BE ADDED winsound beep 

    cv2.imshow('FRAME', resizedFrame)
    cv2.imshow('MASK', fgmask)

    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
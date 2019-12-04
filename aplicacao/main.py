import cv2
import numpy as np
import pytesseract as tess
import imutils
import re
import requests

webcam = False
filename = './files/video.mp4'
degrees = 270


def returnCarPlate(img_org):

    size = np.shape(img_org)
    if size[0] <= 776:
        img_org = imutils.resize(img_org, 900)

    img_org2 = img_org.copy()
    img_bw = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)

    ret3, img_thr = cv2.threshold(img_bw, 125, 255, cv2.THRESH_BINARY)

    img_edg = cv2.Canny(img_thr, 100, 200)

    kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, (7, 7))
    img_dil = cv2.dilate(img_edg, kernel, iterations=1)

    _, contours, _ = cv2.findContours(img_dil.copy(), 1, 2)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    screenCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        return None

    mask = np.zeros(img_bw.shape, dtype=np.uint8)
    roi_corners = np.array(screenCnt, dtype=np.int32)
    ignore_mask_color = (255,)*1

    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    cv2.drawContours(img_org, [screenCnt], -40, (100, 255, 100), 9)

    ys = [screenCnt[0, 0, 1], screenCnt[1, 0, 1],
          screenCnt[2, 0, 1], screenCnt[3, 0, 1]]
    xs = [screenCnt[0, 0, 0], screenCnt[1, 0, 0],
          screenCnt[2, 0, 0], screenCnt[3, 0, 0]]

    ys_sorted_index = np.argsort(ys)
    xs_sorted_index = np.argsort(xs)

    x1 = screenCnt[xs_sorted_index[0], 0, 0]
    x2 = screenCnt[xs_sorted_index[3], 0, 0]

    y1 = screenCnt[ys_sorted_index[0], 0, 1]
    y2 = screenCnt[ys_sorted_index[3], 0, 1]

    return img_org2[y1:y2, x1:x2]


def returnTextPlate(carPlateImg):

    # tess.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    text = tess.image_to_string(carPlateImg, lang='eng')

    return re.sub('[^A-Z0-9]+', '', text)


def saveCarPlate(carPlateText):

    if carPlateText != '':

        r = requests.post("http://localhost:8000/logs/" + carPlateText)

        if r.status_code == 200:
            return True

    return False


cap = cv2.VideoCapture(filename)

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True:

        img = imutils.rotate(frame, degrees)
        cv2.imshow('video', img)

        try:
            carPlateImg = returnCarPlate(img)

            if carPlateImg is not None:
                carPlateText = returnTextPlate(carPlateImg)
                print(carPlateText)

                carPlateText = returnTextPlate(carPlateImg)
                # saveCarPlate(carPlateText)

        except:
            print("Error")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

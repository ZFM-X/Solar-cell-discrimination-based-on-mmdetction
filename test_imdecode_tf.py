import cv2


image_grayscale = cv2.imdecode(np.fromfile(img_fullname, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
image_grayscale = cv2.resize(image_grayscale, (1024, 1024))

image_bgr = cv2.imdecode(np.fromfile(img_fullname, dtype=np.uint8), cv2.IMREAD_COLOR)
if image_grayscale.shape[0] != 800:  #halm  1200
    image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
    image_bgr = cv2.resize(image_bgr, (1024, 1024))
if image_grayscale.shape[0] == 800:   #力禧特
    image_grayscale = cv2.transpose(image_grayscale)
    image_grayscale = cv2.flip(image_grayscale, 1)
    image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
    image_bgr = cv2.resize(image_bgr, (1024, 1024))
    image_bgr = cv2.transpose(image_bgr)
    image_bgr = cv2.flip(image_bgr, 1)
import cv2
import numpy as np


# image_grayscale = cv2.imdecode(np.fromfile(r'F:\peter_share\Peter\zhuhai\OK\20A20ABIN134_1750821403_221_NG_147_plain.jpg', dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
image_grayscale = cv2.imdecode(np.fromfile(r'F:\peter_share\Peter\zhuhai\OK\20A20ABIN134_1750821403_221_NG_147_plain.jpg', dtype=np.uint8), cv2.IMREAD_COLOR)
image_grayscale = cv2.resize(image_grayscale, (1024, 1024))


print(image_grayscale.shape)

cv2.imshow("image", image_grayscale) # 显示图片，后面会讲解
cv2.waitKey(0) #等待按键

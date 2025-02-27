import os

import cv2
import numpy as np
import torchvision.utils as vutils


root_path = r'C:\Users\Admin\Desktop\20221130\test_el_test_1024_test10'

img_real_path = os.path.join(root_path, '0_image_real.jpg')
img_rec_path = os.path.join(root_path, '0_image_rec.jpg')
img_sub_path = os.path.join(root_path, '0_image_rec_err.jpg')


img_real = cv2.imread(img_real_path)#.astype(np.int16)
img_rec = cv2.imread(img_rec_path)#.astype(np.int16)
img_sub = cv2.imread(img_sub_path)#.astype(np.int16)
# img_sub = 255 - img_sub

# img_arg = np.concatenate((img_real[:, :, 0:2] , np.expand_dims(img_sub[:,:,0]-112, 2)), 2)



# # img_rgo = np.concatenate((img_real[:, :, 0:2] , 255-np.expand_dims(img_sub[:,:,0], 2)), 2)
# # img_rgo = np.concatenate((img_real[:, :, 0:2] , np.expand_dims(np.abs(img_real[:, :, 0]-img_rec[:, :, 0]), 2)), 2)
# sub = np.expand_dims(np.abs(img_real[:, :, 0]-img_rec[:, :, 0]), 2)
# # sub = np.abs(img_real.astype(np.int16)-img_rec.astype(np.int16))#.astype(np.uint8)
sub = np.abs(img_real-img_rec)#.astype(np.uint8)


img_real_mean = img_real.mean()
sub_mean = sub.mean()
total_mean = img_real_mean + sub_mean

# # 放大重构误差到真图灰度
# sub = (img_real_mean / sub_mean) * sub

# real_ratio = 0.99
# sub_ratio = 1 - real_ratio

# img_real = (1 + sub_ratio) * img_real
# sub = sub_ratio * sub


# # img_arg = (img_real * (img_real_mean/total_mean) + sub * (sub_mean/total_mean)).astype(np.uint8)
# img_arg = (img_real - sub).astype(np.uint8)


# img_arg = (img_real * (1-(sub.mean()/img_real.mean()))) + sub

# img_rgo = np.concatenate((img_real[:, :, 0:2] , np.expand_dims(np.abs(img_real[:, :, 0]-img_rec[:, :, 0]), 2)), 2)

# vutils.save_image(
#     img_sub,
#     '{}\\{}_image_arg.jpg'.format(root_path, 'test'), nrow=8
#     # torch.cat([real_batch[:max_imgs], rec_det[:max_imgs], fake[:max_imgs]], dim=0).data.cpu(),
#     # '{}/image_{}.jpg'.format(fig_dir, cur_iter), nrow=num_row
# )


# img_sub = np.abs(img_real-img_rec)


cv2.imshow('img_real', img_real)
cv2.imshow('img_rec', img_rec)
cv2.imshow('img_sub', img_sub)
cv2.imshow('img_arg', img_arg)
cv2.waitKey(0)

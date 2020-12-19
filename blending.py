# -*- coding: utf-8 -*-
"""Blending.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15H24VAEFYDEPIFntpc1eksPS9QZcHNZ9
"""


import numpy as np
import math,cv2

PATH = '/INT3404_21-N6/Motherboard-hardware/'
OUTPATH = '/INT3404_21-N6/result_blending/'
pi = math.pi

def N(x,micro,sigma):
    res = []
    d = -((x-micro)*(x-micro))/(2*sigma*sigma)
    for dx in d:
        res.append(math.exp(dx)/(sigma*math.sqrt(2*pi)))
    return np.array(res)

def weight_alpha(x,lam,sigma,micro,c):
    res_a = lam*N(x,micro,sigma)+c
    return res_a

#1000-5000
lam = 1000
#20-60
sigma = 20
#20-40
c = 40
micro = 128

gain_shifted = []
weight_alphas = []

for k in range(1,17):
    img = cv2.imread(PATH+"mb_"+str(k)+".jpg")
    gain_shifted.append(img)
    weight_alphas.append(img)

gain_shifted = np.array(gain_shifted)
print(gain_shifted.shape)
result = np.zeros_like(gain_shifted)
result = result.astype(np.float64)
print(result.dtype)
k = 0

for img in gain_shifted:
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pix_vl = weight_alpha(img[i][j],lam,sigma,micro,c)
            weight_alphas[k][i][j] = pix_vl
    k = k + 1

k = 0

weight_sum = np.sum(weight_alphas)
print(weight_sum)
test_sum = 0
for img in gain_shifted:
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
          weight_beta = weight_alphas[k][i][j]/weight_sum
          test_sum = test_sum + weight_beta
          result[k][i][j] =weight_beta*img[i][j]
    k = k + 1 
print(test_sum)
print(type(result))
print(np.sum(result))
img_res = np.zeros([result.shape[1],result.shape[2],result.shape[3]])

for img in result:
    img_res = np.add(img_res,img)
print(img_res)
img_n = cv2.normalize(src=img_res, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
cv2.imwrite(OUTPATH+'result_norm.jpg',img_n)
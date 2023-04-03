'''
实现opencv-python读取摄像头的数据，并且逐帧分析，识别二维码的项目需求
QR二维码是现实生活中常见的二维码之一，用于支付和乘车

author:
hua

项目描述：
points包含QR二维码的最小区域四边形的四个顶点坐标，即二维码的四个顶点坐标。结果以字符串的形式返回。
当滑动窗口在图片上滑动时，从最小的滑动窗口一直到大的窗口，从而找出图像的特征以及二值化的一些特征，此项目中先找到图片的顶点坐标的特征点
然后进行识别解码处理
'''
# -*-coding:utf-8 -*-
import cv2

import numpy 

cv2.namedWindow("window_for_QR",0)

cv2.resizeWindow("window_for_QR", 640, 480)


cap = cv2.VideoCapture(0)#cv模块下的一个类创建类的对象，即开启摄像头
#videocapture的参数为文件名字，可以设置为一个0


print('摄像头是否开启：{}'.format(cap.isOpened()))#1，格式化字符串   2，显示摄像头是否打开

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)#调节摄像头的分辨率，即为摄像头的分辨率
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)


print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print('setfps', cap.set(cv2.CAP_PROP_FPS, 30))#打印字符串以及设置的视频流的帧率，每分钟30张
print(cap.get(cv2.CAP_PROP_FPS))


while(True):
    ret, frame = cap.read()  #第一个参数返回一个布尔值（True/False），代表有没有读取到图片；第二个参数表示截取到一帧的图片
    #cv2.imshow('window_for_QR', frame)#即将读取的图片信息每一帧进行一个显示

    # 初始化cv2的二维码检测器
    qrcoder = cv2.QRCodeDetector()
   # qr检测并解码
    codeinfo, points, straight_qrcode = qrcoder.detectAndDecode(frame)
# 绘制qr的检测结果
    if points is not None:
     cv2.drawContours(frame, [numpy.int32(points)], 0, (0, 0, 255), 2)#opencv画图像的一些工具，对原图进行操作，选择轮廓，选择颜色和线宽
     print(points)

# 打印解码结果
    if codeinfo is not None:
     print("qrcode :", codeinfo)
     cv2.imshow('window_for_QR', frame)#即将读取的图片信息每一帧进行一个显示


#每一帧进行opencv二维码的检测
    if cv2.waitKey(1) & 0xFF == ord('q'):  #waitkey方法，当delay参数小于0的时候，则堵塞一直等待按键，当大于0时，为等待的ms数
         break
  
#当退出代码进程的时候，即释放类对象的内存，并消除窗口
cap.release()#解放视频
cv2.destroyAllWindows()




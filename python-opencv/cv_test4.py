'''
本作品用opencv实现了检测形状的项目功能

思路：先角点检测，实现人工提取特征，先canny算子进行边缘检测，
然后检测角点之类的，识别检测的形状。

进行简单提取特征，并且自定义其判别方式的算法

author:hua

其中 cv.approxPolyDP() 的参数1是源图像的某个轮廓；参数2(epsilon)是一个距离值，
表示多边形的轮廓接近实际轮廓的程度，
值越小，越精确；参数3表示是否闭合。



cv2.findContours()函数首先返回一个list，
list中每个元素都是图像中的一个轮廓，用numpy中的ndarray表示。
这个概念非常重要。在下面drawContours中会看见。

'''
# -*-coding:utf-8 -*-
import cv2
import numpy 

'''用于测试一行代码'''
a = numpy.array([[0,2]])
print(a[0])

def  NO():
  pass 

cv2.namedWindow("shape",0)
cv2.resizeWindow("shape", 640, 480)#设置窗口的大小


cv2.namedWindow("parameter",0)
cv2.resizeWindow("parameter", 640, 480)#设置窗口的大小
cv2.createTrackbar('Threadhold1','parameter',100,255,NO)#创建一个相应的图形化的状态栏，可以进行手动调试的，有一个回调函数
cv2.createTrackbar('Threadhold2','parameter',100,255,NO)

cv2.createTrackbar('Threadhold3','parameter',5000,30000,NO)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)#调节摄像头的分辨率，即为摄像头的分辨率
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
print('setfps', cap.set(cv2.CAP_PROP_FPS, 30))#打印字符串以及设置的视频流的帧率，每分钟30张

def ShapeDetection(img):                 
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  #寻找轮廓，根据之前的边沿检测的图像而得，有返回值
    #得到的轮廓是闭合曲线
    
    
    #contours是返回的轮廓，hierarchy是每条轮廓对应的属性
    #print(contours)#存储的数组元素
    #print(numpy.size(contours)) #   得到该图中总的轮廓数量
    #print(contours[0])#返回的是每个轮廓的点的集合
    for obj in contours:
        area = cv2.contourArea(obj)  #计算轮廓内区域的面积，可以剔除一些杂波
        threadhold3 = cv2.getTrackbarPos('Threadhold3','parameter')
        if area > threadhold3:
         cv2.drawContours(imgContour, obj, -1, (255, 0, 0), 4)  #绘制轮廓线
         perimeter = cv2.arcLength(obj,True)  #计算轮廓长度
         approx = cv2.approxPolyDP(obj,0.02*perimeter,True)  #获取轮廓角点坐标
         CornerNum = len(approx)  
          #轮廓角点的数量 #轮廓对象分类
         if CornerNum ==3: 
             objType ="triangle"
         elif CornerNum == 4:
             if w==h: 
                objType= "Square"
             else:objType="Rectangle"
         elif CornerNum>10:
             objType= "Circle"
            #print(x,y)#如果识别出圆形物体，则返回坐标值
             x, y, w, h = cv2.boundingRect(approx)  #获取坐标值和宽度、高度，即用一个边框进行一个设定
             cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,0,255),2)  #绘制边界框
             cv2.putText(imgContour,objType,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)  #绘制文字
         else:objType="N"
        
        else:
          pass
          
while(True):
    ret, frame = cap.read()  #第一个参数返回一个布尔值（True/False），代表有没有读取到图片；第二个参数表示截取到一帧的图片
    imgContour = frame.copy()
    imgGray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)  #转灰度图
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)  #高斯模糊，高斯算子，进行图像的空间范围的滤波

    threadhold1=cv2.getTrackbarPos('Threadhold1','parameter')
    threadhold2=cv2.getTrackbarPos('Threadhold2','parameter')

    imgCanny = cv2.Canny(imgBlur,threadhold1,threadhold2)  #Canny算子边缘检测
    
    kenel = numpy.ones((5,5))
    imgCanny = cv2.dilate(imgCanny, kenel, iterations=2) #进行图像的膨胀，使用kenel的5x5的核进行处理，处理5次，进行毛刺的提取

    #参数为阈值，进行一个边缘的阈值分析

    ShapeDetection(imgCanny)
    #cv2.imshow("shape",imgContour)#显示有图形化的界面
    cv2.imshow("shape Detection", imgContour)#显示识别出的效果


    if cv2.waitKey(1) & 0xFF == ord('q'):
     break

#当退出代码进程的时候，即释放类对象的内存，并消除窗口
cap.release()#解放视频
cv2.destroyAllWindows()
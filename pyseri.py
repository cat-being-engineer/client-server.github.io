
'''查看串口的程序，Serial模块下的Serial函数起到打开串口的功能,查看哪个串口得到了数据'''
from serial.tools import list_ports
import serial
  
if __name__ == '__main__':
    # 获取端口列表，列表中为 ListPortInfo 对象，获取所有的端口
     port_list = list(list_ports.comports())
     num = len(port_list)
     a =0
if num <= 0:
        print("找不到任何串口设备")

else:

  for i in range(num):
            # 将 ListPortInfo 对象转化为 list
              port = list(port_list[i])
              #为了防止串口打开的报错，try  except的查错用法
              try:
               SER=serial.Serial(port[0],115200,timeout=0.5) #使连接串行口,设置了延时时间，在python中第一个元素为0下标，不同于matlab   
               s = SER.read(1)#从端口读2个字节
               if(s != '\0'):   #当读取有数的时候
                    print(port[0])
               SER.close()
              except(OSError, serial.SerialException):#当tty文件无法正常打开时，即被其他的程序所占用时   
                      pass
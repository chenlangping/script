# pip install opencv-python
import cv2
# 读取视频
video = cv2.VideoCapture('test.flv')
# 逐帧读取，当还有画面时ret为True，frame为当前帧的ndarray对象
ret, frame = video.read()
i = 0
# 循环读取
while ret:
    i += 1
    cv2.imwrite('picture_'+str(i) + '.jpg', frame)
    ret, frame = video.read()
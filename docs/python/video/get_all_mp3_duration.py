# pip install eyed3
import os
import eyed3

dir = 'E:\\BaiduNetdiskDownload\\【零号基地144】趣谈Linux操作系统（完结）\\mp3\\'
files = os.listdir(dir)

sum = 0
count = 0
for file in files:
    mp3_file = dir + file
    sum += eyed3.load(mp3_file).info.time_secs
    count +=1
print("sum seconds = " + str(sum))
print("mp3 count = " + str(count))
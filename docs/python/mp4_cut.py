# pip install moviepy
from moviepy.editor import *

video = VideoFileClip('test.flv')

# get first 30 seconds
new_video = video.subclip(0, 10)

# remove last 30 seconds
# video.subclip(0, video.duration-30)

# output
new_video.write_videofile('test2.mp4',verbose=False,audio = False)
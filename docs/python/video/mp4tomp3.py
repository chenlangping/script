# pip install moviepy
from moviepy.editor import *

video = VideoFileClip('test.mp4')
audio = video.audio
audio.write_audiofile('test.mp3')
import os
import types
import uuid

import eyed3

dir = 'F:\\test\\mp3\\'

# title 标题
# artist 参与创作的艺术家
# album 专辑，唱片集
def edit_mp3_meta(path, artist, album, title):    
    audiofile = eyed3.load(path)
    if audiofile != None:
        audiofile.initTag()
        audiofile.tag.artist = u'%s' % artist
        audiofile.tag.album = u'%s' % album
        audiofile.tag.title = u'%s' % title
        audiofile.tag.save()

if __name__ == "__main__":
    dirs = os.listdir(dir)
    for file in dirs:
        path = dir + file
        edit_mp3_meta(path, title=file, artist='vscode', album='vscode')

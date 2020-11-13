import os
import types
import uuid

import eyed3

dir = 'F:\\Test\\mp3\\'


def __rename(path, new_name=uuid.uuid4()):
    if os.path.exists(path):
        filename = os.path.basename(path)
        if len(filename) > 0 and filename.index('.') < len(filename):
            base_path = os.path.dirname(path)
            suffix = filename.split('.')[1]
            rename = (base_path + '\\{}.' + suffix).format(str(new_name).replace('-', ''))
            if os.path.exists(rename):
                rename = (base_path + '\\{}.' + suffix).format(str(uuid.uuid4()).replace('-', ''))
            os.rename(path, rename)
            return rename
    else:
        print(path + 'not found!')


# artist 参与创作的艺术家
# album 专辑，唱片集
# title 标题
def edit_mp3_meta(path, artist, album, title):
    filename = os.path.basename(path).split('.')[0]
    path = __rename(path)
    try:
        audiofile = eyed3.load(path)
        if audiofile != None:
            audiofile.initTag()
            audiofile.tag.artist = u'%s' % artist
            audiofile.tag.album = u'%s' % album
            audiofile.tag.title = u'%s' % title
            audiofile.tag.save()
    finally:
        __rename(path, filename)


if __name__ == "__main__":
    dirs = os.listdir(dir)
    for file in dirs:
        path = dir + file
        edit_mp3_meta(path, title=file, artist='艺术家', album='专辑')

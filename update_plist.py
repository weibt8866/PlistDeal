#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 导出资源
# pip xmltodict
# pip Pillow

from ast import literal_eval
import imp
from pickletools import optimize
from posixpath import split
from re import S
import zipfile
import sys
import os
import shutil
import json
import types
# import xmltodict
import plistlib

from xml.dom.minidom import parseString
from PIL import Image, ImageDraw

# import Image

pics = {}


def walkPics(current_dir, our_fir):
    tmpOutPath = our_fir + '/out/'
    if not os.path.exists(tmpOutPath):
        #os.makedirs(tmpOutPath)
        i = 0
    for root, dirs, files in os.walk(current_dir):
        # 遍历文件
        for f in files:
            filePath = os.path.join(root, f)
            file_f = os.path.splitext(f)
            filename, ftype = file_f
            if ftype == ".plist":
                fname = filename
                print('filePath:{filePath}')
                pdict = plistlib.readPlist(filePath)
                src_pic = filename + ".png"
                old_pic = filename+"_copy.png";
                if os.path.exists(src_pic):
                    img = Image.open(src_pic)
                    if os.path.exists(old_pic):
                        os.remove(old_pic)
                    newImg = Image.new('RGBA', (img.width, img.height), (0, 0, 0, 0))
                    frames = pdict["frames"]
                    for name in frames:
                        nFile = os.path.join(root, name)
                        tmpFileName, tmpType = os.path.splitext(name);
                        copyFile = os.path.join(root, f'{tmpFileName}_bk{tmpType}')
                        if os.path.exists(nFile):
                            sPic = Image.open(nFile)
                            info = frames[name]
                            print(f'info==>{info}')
                            print(info['textureRect'], type(info['textureRect']))
                            rotated = info['textureRotated']
                            tmpOffset = info['spriteOffset']
                            tmpOffset = tmpOffset.replace("{", "")
                            tmpOffset = tmpOffset.replace("}", "")
                            tmpOffset = f'[{tmpOffset}]'
                            offset = literal_eval(tmpOffset)
                            tmpOriginalSize = info['spriteSourceSize']
                            tmpOriginalSize = tmpOriginalSize.replace("{", "")
                            tmpOriginalSize = tmpOriginalSize.replace("}", "")
                            tmpOriginalSize = f'[{tmpOriginalSize}]'
                            originalSize = literal_eval(tmpOriginalSize)
                            tmpRect = info['textureRect']
                            tmpRect = tmpRect.replace("{", "")
                            tmpRect = tmpRect.replace("}", "")
                            tmpRect = f'[{tmpRect}]'
                            rect = literal_eval(tmpRect)
                            print(f'rect:{rect}, originalSize:{originalSize}, offset:{offset}, rotated:{rotated}')
                            box = (rect[0], rect[1], rect[0] + (rect[2] if not rotated else rect[3]),
                                   rect[1] + (rect[3] if not rotated else rect[2]))
                            box = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
                            if name=="common_logo_suduku.png":
                                i = 0
                            offx = originalSize[0] / 2 - offset[0] - rect[2] / 2
                            offy = originalSize[1] / 2 - offset[1] - rect[3] / 2
                            box = (offx, offy, offx+rect[2], offy+rect[3])
                            boxCopy = sPic.crop(box)
                            boxCopy.save(copyFile, optimize=True, quality=100)
                            if os.path.exists(copyFile):
                                os.remove(copyFile)
                            if rotated:
                                boxCopy = boxCopy.transpose(Image.ROTATE_270)
                                print(f'new===>w:{boxCopy.width}, h:{boxCopy.height}')

                            print(f'offx:{offx}, offy:{offy}')
                            newImg.paste(boxCopy, (int(rect[0]), int(rect[1])))
                    os.rename(src_pic, old_pic)
                    newImg.save(src_pic, optimize=True, quality=100)
                else:
                    print(f"have not plist:{filename}' pic")

        # 遍历所有的文件夹
        for d in dirs:
            syb_dir = os.path.join(root, d)
            walkPics(syb_dir, our_fir)


current_dir = os.path.abspath(os.path.dirname(__file__))
print(current_dir)
tmpOutPath = current_dir + f'/out/'
#if not os.path.exists(tmpOutPath):
    #os.makedirs(tmpOutPath)
walkPics(current_dir, current_dir)
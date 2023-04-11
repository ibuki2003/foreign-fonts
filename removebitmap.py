#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from https://github.com/tkumata/RemoveBitmapFont/blob/master/removebitmap.py

"""
Usage: python %s path
   argv[1] ... path
eg. python removebitmap.py ~/Downloads/fonts
"""

import sys
import glob
import fontforge
import tempfile
import os
import shutil

# fontforge setting.
fontforge.setPrefs('CoverageFormatsAllowed', 1)
fontforge.setPrefs('UndoDepth', 0)


# TTF flags
flags = ('opentype', 'round')


"""
antialias: Hints are not applied, use grayscale smoothing.
gridfit: Use hinting in Windows.
gridfit+smoothing: ClearType GridFitting; (hinting with ClearType).
symmetric-smoothing: ClearType Antialiasing; (ClearType smoothing only).

gridfit is hinting on Windows. So gridfit is unnecessary for me.
"""
def gasp():
    return (
        (65535, ('antialias', 'symmetric-smoothing')),
    )


"""
@return: list
"""
def fontsSearch(dir, *exts):
    files = []
    dir = os.path.abspath(os.path.expanduser(dir))
    for ext in exts:
        files.extend(glob.glob(dir + '/' + ext))
    return files


"""
Main function
"""
def main(argvs):
    # Set work and save director. Please apply these to your environment.
    # saveDir = workDir + "/new"

    # if not os.path.exists(saveDir):
    #     os.makedirs(saveDir)


    """
    DO NOT CHANGE BELLOW.
    """
    argc = len(argvs)

    if argc != 3:
        quit()

    # TrueType 系統のファイルを探す。
    # fontFiles = fontsSearch(argvs[1], '*.ttc', '*.ttf')

    # 見つかった TrueType 系統のファイルを順次変換する。
    # for fontFile in fontFiles:
    srcFile = argvs[1]
    dstFile = argvs[2]
    if True:
        # set variables.
        fontFSName = os.path.basename(srcFile)
        tmpPrefix = "breakttc"
        tempDir = tempfile.mkdtemp()

        # Get packed family names
        familyNames = fontforge.fontsInFile(srcFile)
        i = 0

        if len(familyNames) == 0:
            familyNames = [""]

        new_files = []

        # Break a TTC to some TTFs.
        for familyName in familyNames:
            # openName format: "msgothic.ttc(MS UI Gothic)"
            print("%s" % familyName)
            if len(familyName) > 1:
                openName = "%s(%s)" % (srcFile, familyName)
            else:
                openName = srcFile

            # tmp file name: breakttf0a.ttf and breakttf1a.ttf and so on.
            tmpTTF = "%s%da.ttf" % (tmpPrefix, i)

            # Open font
            try:
                font = fontforge.open(openName, 32)
            except Exception as e:
                print(e)
                return
            print(font)

            # Edit font
            font.encoding = 'UnicodeFull'
            font.gasp = gasp()
            font.gasp_version = 1
            font.os2_vendor = "maud"
            font.os2_version = 1 # Windows で幅広問題を回避する。

            # ttf へ一時的に保存する。
            font.generate(tempDir + "/" + tmpTTF, flags=flags)
            if os.path.exists(tempDir + "/" + tmpTTF):
                new_files.append(tempDir + "/" + tmpTTF)
            font.close()
            i += 1

        if len(new_files) == 0:
            print("error: empty")
            return


        # set variables.
        newTTCname = fontFSName
        newFontPath = tempDir + "/" + newTTCname
        saveFontPath = dstFile
        files = new_files

        f = fontforge.open(files[0])
        files.pop(0)

        if len(files) > 0:
            f.generateTtc(
                newFontPath,
                [ fontforge.open(file) for file in files ],
                ttcflags=("merge",),
                layer=1)
        elif len(files) == 0:
            f.generate(newFontPath, flags=flags)


        # 新しく生成した分のフォントを閉じる。
        f.close()
        print("saved to ",newFontPath)

        # temporary 内の ttc ファイルを保存先へ移動する。
        if os.path.exists(newFontPath):
            shutil.move(newFontPath, saveFontPath)
        else:
            print("Error: %s is not found." % newFontPath)

        # temporary directory を掃除しておく。
        shutil.rmtree(tempDir)

    # Finish

if __name__ == '__main__':
    main(sys.argv)

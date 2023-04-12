import fontforge
import sys
import pathlib

def main(srcdir, dstdir):
    srcdir = pathlib.Path(srcdir)
    dstdir = pathlib.Path(dstdir)

    for infile in filter(lambda x: x.is_file(), srcdir.glob('**/*')):
        suf = dst_ext(infile)
        if suf is None:
            print("skipping", infile)
            continue

        outfile = dstdir / infile.relative_to(srcdir)
        outfile = outfile.with_suffix(suf)
        outfile.parent.mkdir(parents=True, exist_ok=True)

        if outfile.exists():
            continue

        try:
            conv(infile, outfile)
        except Exception as e:
            print(e)
            continue


def dst_ext(srcfile):
    if srcfile.suffix == '.dfont':
        return '.ttf'

    fonts = fontforge.fontsInFile(str(srcfile))
    if len(fonts) > 1:
        return ".ttc"
    elif len(fonts) == 1:
        if srcfile.suffix:
            if srcfile.suffix == '.fon':
                return '.ttf'
            return srcfile.suffix
        else:
            f = fontforge.open(str(srcfile))
            q = f.is_quadratic
            f.close()
            return '.ttf' if q else '.otf'
    else:
        return None


def conv(infile, outfile):
    print(infile, outfile)
    fonts = fontforge.fontsInFile(str(infile))
    print(fonts)

    if len(fonts) > 1:
        newfonts = []

        for i, font in enumerate(fonts):
            f = fontforge.open("{}({})".format(str(infile), i), 1 | 16)
            print(font)
            f.familyname = font
            newfonts.append(f)

        newfonts[0].generateTtc(
            str(outfile),
            newfonts[1:],
            ttcflags=("merge",),
            bitmap_type="",
            layer=1)
        for f in newfonts:
            f.close()
    else:
        f = fontforge.open(str(infile), 1 | 16)
        f.generate(str(outfile), bitmap_type="")
        f.close()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

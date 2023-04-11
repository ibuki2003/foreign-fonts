# Fonts package builder

Make a package with fonts from Windows or MacOS.
Additionally, remove bitmap fonts from them so that they can be rendered clearly.

## usage

```sh
cp /path/to/font.ttf ./orig/hoge/a.ttf
./conv.bash
makepkg -Ri
ls /usr/share/fonts/hoge/a.ttf
```

## requirements

- fontforge with python


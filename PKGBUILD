pkgname='foreign-fonts'
pkgdesc='Fonts from other OSes'
pkgver=0.0.2
pkgrel=1
arch=('any')

source=()
md5sums=()

prepare() {
  return 1
}

build() {
  return 1
}

package() {
  ls -la "$srcdir" "$pkgdir"
  mkdir -p "$pkgdir/usr/share/fonts"
  cp -r "$srcdir/files"/* "$pkgdir/usr/share/fonts"
}

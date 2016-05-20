#! /bin/bash

make install

version=$(git log -1 --format='%cd.%h' --date=short | sed 's/-//g')

dch -v "0.1+$version" ''

dpkg-buildpackage -us -uc

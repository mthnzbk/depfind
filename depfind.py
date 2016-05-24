#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pisi.db.filesdb import FilesDB
import re
import sys

dep_tag = "<Dependency>%s</Dependency>"

cmake_file = sys.argv[1]

package_list = []

with open(cmake_file) as file_cmake:
    # dosya satır satır okunuyor ve istenilen veriler ayıklanıyor.
    for line in file_cmake.readlines():
        compile = re.compile(r"^find_package\((.*) +[0-9][A-Z]\)")
        obje = compile.search(line)

        if obje:
            # istenilen veri varsa listeye ekliyoruz.
            package_list.append(obje.groups()[0].split(" ")[0])

        compile = re.compile(r"^find_package\((.*)\)\n")
        obje = compile.search(line)

        if obje:
            # istenilen veri varsa listeye ekliyoruz.
            package_list.append(obje.groups()[0].split(" ")[0])

files_db = FilesDB()

print package_list # Aranacak verileri yazdırıyoruz.

counter = 0
packages = []

for package in package_list:
    liste = files_db.search_file(package)

    # aranan veri değer döndürürse döngü başlar
    if liste:
        for li in liste:
            for l in li[-1]:
                # dosyaların uzantısı *.cmake olanları ayıklayıp çıktı veriyoruz.
                if l.startswith("usr/lib/cmake/%s/" % package) and l.endswith("cmake"):
                    print package, "-", li[0], "-", l
                    counter += 1  # sayaç ile cmake dosyalarının varlığı tespit ediliyor.
                    packages.append(li[0])

                if not counter:
                    print package, "-", u"Bulunamadı"

                else:
                    counter = 0

    else:
        print package, "-", u"Bulunamadı"

for package in set(packages):
    print dep_tag % package
#-*- coding: utf-8 -*-
#!/usr/bin/env python

from pisi.db.filesdb import FilesDB
import sys
import re

dep_tag = "<Dependency>{}</<Dependency>"

cmake_file = sys.argv[1]


package_list = []
# find_package(Qt5 $

with open(cmake_file) as file_cmake:
	# dosya satır satır okunuyor ve istenilen veriler ayıklanıyor.
	for line in file_cmake.readlines():
		compile = re.compile(r"^find_package\((.*) \$")
		obje = compile.search(line)
		if obje:
			# istenilen veri varsa listeye ekliyoruz.
			package_list.append(obje.groups()[0])

files_db = FilesDB()

print package_list # Aranacak verileri yazdırıyoruz.

counter = 0

for package in package_list:
	liste = files_db.search_file(package)

	#aranan veri değer döndürürse döngü başlar
	if liste:
		# liste içinde liste.
		for li in liste:
			# ilk liste ögesi(li[0]) paket adı, ikincisi de(li[-1]) liste halinde aranan kelimenin geçtiği dosyalar.
			for l in li[-1]:
				# dosyaların uzantısı *.cmake olanları ayıklayıp çıktı veriyoruz.
				if l.startswith("/usr/lib/cmake/%s"%package) and l.endswith("cmake"):
					print package, "-", li[0], "-", l
					counter += 1 # sayaç ile cmake dosyalarının varlığı tespit ediliyor.
		# sayaç artmamışsa demekki cmake dosyası yoktur ve bunun bilgisi çıktıya yansır.
		if not counter:
			print package, "-", u"Bulunamadı"
		# sayaç artmışsa sıfırlanır ki bir sonraki döngü de hata oluşmasın.
		else:
			counter = 0

	# liste boş ise aranan veriye sahip paket kurulu değildir.
	else:
		print package, "-", u"Bulunamadı"
			
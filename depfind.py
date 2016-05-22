from pisi.db.filesdb import FilesDB
import sys
import re

dep_tag = "<Dependency>{}</<Dependency>"

cmake_file = sys.argv[1]


package_list = []
# find_package(Qt5 $

with open(cmake_file) as file_cmake:
	for line in file_cmake.readlines():
		compile = re.compile(r"^find_package\((.*) \$")
		obje = compile.search(line)
		if obje:
			package_list.append(obje.groups()[0])


print package_list
files_db = FilesDB()


for package in package_list:
	liste = files_db.search_file(package)
	for l in liste:
		for li in l[-1]:
			if li.endswith("cmake"):
				print package, "-", l[0], "-", li
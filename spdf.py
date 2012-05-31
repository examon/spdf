#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Tomas Meszaros <exo [at] tty [dot] sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------
#
# DESCRIPTION:
#
# spdf is a simple program which can split pdf file into two
#
#
# --------------------------------------------------------------------
#
# DEPENDENCES:
#
#	pyPdf
#
# pyPdf can be found at http://pybrary.net/pyPdf/
#
# --------------------------------------------------------------------
#
# USAGE:
#
# $ python spdf.py source.pdf pagenumber
#
# pagenumber: page number in source.pdf, where you want to split it
#
# source.pdf will be splitted automatically into two parts:
#
#	source_part1.pdf
#	source_part2.pdf

from pyPdf import PdfFileWriter, PdfFileReader
from sys import argv

def main():
	split_page = int(argv[2])

	# try load source.pdf to source[]
	source = []
	try: source.append(PdfFileReader(file(argv[1], "rb")))
	except IOError:
		print "error: file \"%s\" does not exist" % argv[1]
		return

	# check if pagenumber is a valid number
	if (split_page > source[0].getNumPages()):
		print "error: page number \"%d\" does not exist in \"%s\"" \
				% (split_page, argv[1])
		return

	# make names for both parts
	part1 = argv[1].split('.')[0] + "_part1.pdf"
	part2 = argv[1].split('.')[0] + "_part2.pdf"

	# take source.pdf and split it
	first_output = PdfFileWriter()
	second_output = PdfFileWriter()
	for i in range(source[0].getNumPages()):
		if (i >= split_page): second_output.addPage(source[0].getPage(i))
		else: first_output.addPage(source[0].getPage(i))
	
	# save first_output to part1
	outputStream = file(part1, "wb")
	first_output.write(outputStream)
	outputStream.close()
	
	# save second_output to part2
	outputStream = file(part2, "wb")
	second_output.write(outputStream)
	outputStream.close()

def show_help():
	print "USAGE: %s source.pdf pagenumber" % argv[0]
	print "pagenumber: page number in source.pdf"

if __name__ == "__main__":
	if (len(argv) == 3) and argv[2].isdigit(): main()
	else: show_help()

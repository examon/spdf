#!/usr/bin/env python2
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
#	PyPDF2
#
# PyPDF2 can be found at http://mstamy2.github.io/PyPDF2/
#
# --------------------------------------------------------------------
#
# USAGE:
#
# $ python spdf.py source.pdf pagenumber
#
# pagenumber:
#	- page number in source.pdf, where you want to split it
#	- use pagenumber == 0, to split source.pdf into individual pages

from PyPDF2 import PdfFileWriter, PdfFileReader
from sys import argv, exit
from getpass import getpass

def main():
	#last argv that makes pdf split at given page
	split_page = int(argv[2])
	
	# try load source.pdf to source[]
	source = []
	try:
		source.append(PdfFileReader(file(argv[1], "rb")))
	except IOError:
		exit("error: file \"%s\" does not exist" % argv[1])
	
	# check if is source.pdf encrypted
	if (source[0].getIsEncrypted()):
		print "warrning: file \"%s\" is encrypted" % argv[1]
		pw = getpass("decrypt %s, password: " % argv[1])
		if (source[0].decrypt(pw) == 0):
			exit("error: sorry, wrong passowrd")
		else: 
			print "%s has been dencrypted, processing..." % argv[1]
		
	# check if pagenumber is a valid number
	if (split_page >= source[0].getNumPages()):
		exit("error: page number \"%d\" does not exist in \"%s\"" % (split_page, argv[1]))

	# make names for both parts
	part1 = argv[1].split('.')[0] + "_part1.pdf"
	part2 = argv[1].split('.')[0] + "_part2.pdf"

	first_output = PdfFileWriter()
	second_output = PdfFileWriter()

	# take source.pdf and split it
	for i in range(source[0].getNumPages()):
		if (split_page == 0):
			# split source.pdf into each page & save it
			page_output = PdfFileWriter()
			page_output.addPage(source[0].getPage(i))
			page_name = argv[1].split('.')[0] + "_page" + str(i+1) + ".pdf"	
			outputStream = file(page_name, "wb")
			page_output.write(outputStream)
			outputStream.close()
		else:	
			# split source.pdf into two parts & save it
			if (i >= split_page): second_output.addPage(source[0].getPage(i))
			else: first_output.addPage(source[0].getPage(i))
		
	# source.pdf is already splitted
	if (split_page == 0):
		print "done!"
		return
	
	# save first_output to part1
	outputStream = file(part1, "wb")
	#try to test is the file is compatible
	try:
		first_output.write(outputStream)
		outputStream.close()
	except:
		print "Error line 102(first_output.write(outputStream), Can't Read this file."
	
	# save second_output to part2
	outputStream = file(part2, "wb")
	#try to test is the file is compatible
	try:
		second_output.write(outputStream)
		outputStream.close()
	except:
		print "Error line 110(second_output.write(outputStream), Can't Read this file."
	print "done!"

def show_help():
	print "USAGE: %s source.pdf pagenumber" % argv[0]
	print "pagenumber:"
	print "  - page number in source.pdf, where you want to split it"
	print "  - use pagenumber == 0, to split source.pdf into individual pages"

if __name__ == "__main__":
	if (len(argv) == 3) and argv[2].isdigit(): main()
	else: show_help()

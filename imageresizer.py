#!/usr/bin/env python

try:
	import Image
except:
	from PIL import Image
import os, glob
import shutil
#========================================================

class Resizer:

	def __init__(self, path, original_folder):
		self.__path = path
		self.__original_folder = original_folder

#--------------------------------------

	def __replace_original(self, im, filename):
		originals_path = os.path.join(os.path.dirname(filename), self.__original_folder) 
		if not os.path.exists(originals_path):
			os.makedirs(originals_path)
		shutil.move(filename, originals_path)
		im.save(filename)

#--------------------------------------
	def __resize_image(self, filename):
		try:
			im = Image.open(filename)
		except:
			im = None

		if not im is None:

			#print im.format, im.size, im.mode

			newdim = 128
			(w, h) = im.size

			if w > newdim or h > newdim:

				print "Resizing ", filename, "from (", w, ", ", h, ") to (", newdim, ", ", newdim, ")"
				im.thumbnail((newdim, newdim)  , Image.ANTIALIAS)
				
				self.__replace_original(im, filename)
				
			else:
				#print "Skipping ", filename, " (", w, ",  ", h, ") "
				pass
				
#--------------------------------------

	def __resize_images_in_folder(self):

		for infile in glob.glob( os.path.join(self.__path, '*') ):
			self.__resize_image(infile) 

#--------------------------------------

	def resize(self):
		if not os.path.exists(self.__path):
			raise Exception( self.__path, " does not exist")
		else:
			if os.path.isdir(self.__path):
				self.__resize_images_in_folder()
			else:
				self.__resize_image(self.__path)

#========================================================
"""
def main():
	#theResizer = Resizer(".", "originals")
	theResizer = Resizer("plex.png", "originals")
	theResizer.resize()
	

if __name__ == "__main__":
    main()
"""

		

import simplekml
import os
import pysrt
import progressbar
from Tkinter import *  
import Tkinter, Tkconstants, tkFileDialog




def main():

	root = Tk()
		
	#-------------------------------srt file selection-----------------------

	root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select srt file",filetypes = (("SRT","*.SRT"),("all files","*.*")))		

	root.file_path = tkFileDialog.asksaveasfilename(initialdir = "/",title = "select directory to save ",filetypes = (("KML file","*.kml"),("all files","*.*")))

	root.destroy()

	#----------loading input (drone flight .srt ) file------------------------------ 
	
	subs = pysrt.open(root.filename)

	#--------------------------------progress bar --------------------------------------

	bar = progressbar.ProgressBar(maxval=170,widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()

	i=0
	#------------------simplekml lib used to generate kml-----------------------
	kml=simplekml.Kml()

	while True:
		try:
			lon,lat,z = subs[i].text.split(",")
			
			#------------adding GPS coordinates to kml-----------------
			
			kml.newpoint(name=str(subs[i].start.hours)+":"+str(subs[i].start.minutes)+":"+str(subs[i].start.seconds),coords=[(float(lat),float(lon))])	
			
			i=i+1
			
			bar.update(i)
			
			kml.save(root.file_path)

		except IndexError:
			break

	bar.finish()

	print "file has been created at  :",root.file_path 

main()	
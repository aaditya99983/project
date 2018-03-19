import math   
import pysrt		
import piexif 	
import csv			
from Tkinter import *  
import Tkinter, Tkconstants, tkFileDialog
import os
import progressbar

#---------------lat,lon to degree conversion-----------------------------------------------
def degrees(value):
	
		 
	d0 = value[0][0]
	d1 = value[0][1]
	d = float(d0) / float(d1)

	m0 = value[1][0]
	m1 = value[1][1]
	m = float(m0) / float(m1)

	s0 = value[2][0]
	s1 = value[2][1]
	s = float(s0) / float(s1)

	return d + (m / 60.0) + (s / 3600.0)

#-------------returns distance b/w two lats and lons(HAVERSINEs FORMULA)-------------------------

def distance(lat1,lon1,lat2,lon2): 
	radius= 6373.0
	dlat = math.radians(lat2-lat1)
	dlon = math.radians(lon2-lon1)
	a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	
	distance = radius * c

	return distance
# -------------------------function to write images(which lie within req distance) -------------------------------------------

def image_writer(lat_drone,lon_drone,max_distance,directory,csv,time):

	csv.write(time) # writing time of present drone location from srt in output.csv 

	for root,subdir,files in os.walk(directory):

		#sorting files(images) according their name as os.walk gives list of files(images) in random order this make output csv more readable

		files.sort() 

		for file in files:

			image = piexif.load(os.path.join(root,file))	#loading images
			
			try:	
				#extracting latitude and longitude
				lat_img=degrees(image['GPS'][piexif.GPSIFD.GPSLongitude])
				lon_img=degrees(image['GPS'][piexif.GPSIFD.GPSLatitude])
			
			except KeyError: # evoked when 'GPS' data of image couldn't be read 
				
				lat_img=None
				lon_img=None
				
			if((lat_img and lon_img)  is not None):

				#-------calculating distance b/w every image and drone coordinate at ith second

				if(int(1000*(distance(lat_drone,lon_drone,lat_img,lon_img)))<max_distance):
					
					image_to_write = "" +"," + file 
				
					csv.write(image_to_write)
			
					
	csv.write(" "+","+"\n")



def main_exec():

	no_vids=raw_input ("how many videos do you want to process  :")

	try:
		
		#-------- progress bar to indicate total work done(in %)---------------------------------------
		
		bar = progressbar.ProgressBar(maxval=170,widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

		
		
		#---------------------GUI for files(.srt,images folder) selection------------------------------
		
		root = Tk()
			
		root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select srt file",filetypes = (("SRT","*.SRT"),("all files","*.*")))		

		root.filename2 = tkFileDialog.asksaveasfilename(initialdir = "/",title = "select directory to save ",filetypes = (("CSV file","*.csv"),("all files","*.*")))

		root.directory = tkFileDialog.askdirectory(initialdir="/",title="please select images folder")

		root.destroy()		
		
		#----------------- output file generation-------------------------------------------------
		csv = open(root.filename2, "a")

		csv.write("time"+","+"images\n")
		# --------------------------------------srt file selection-------------------------------------
		
		subs = pysrt.open(root.filename)

		for no_times in range(int(no_vids)):

			distance_radius=raw_input("give the the distance within which images you want  :")
			
			i=0
			
			try:

				bar.start()

				while int(distance_radius):
					
					try:
						#---------extracting GPS coordinates from subtitles--------------------------
						
						coordinates = subs[i].text.split(",")
						
						#-------- time in  H:M:S:MS (H=hours,M=min,S= seconds,MS=milliseconds)--------
						
						time=str(subs[i].start.hours)+":"+str(subs[i].start.minutes)+":"+str(subs[i].start.seconds)+":"+str(subs[i].start.milliseconds)

						#------- sending drone present coordinates to image_writer fn, so as to calclate distance with other images and write 
						#------- and write corresponding images to output csv 
						
						image_writer(float(coordinates[0]),float(coordinates[1]),int(distance_radius),root.directory,csv,time)
						
						csv.write(" "+","+"\n")	

						i=i+1

						bar.update(i)

					except IndexError:#evoked when distance_radius is not valid entry
						break

				bar.finish()
						
			except ValueError: # evoked when distance_radius is not a valid entry
				print "please enter an integer/float distance next time\n"
				print ".......aborting"			
			
			print "file(.csv) saved at  :",root.filename2
			
	except ValueError: # evoked when no_vids is not a valid entry
		print "please enter an integer next time\n"
		print ".......aborting"

main_exec()
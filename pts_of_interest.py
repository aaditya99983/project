import math   
import pysrt		
import piexif 	
import csv			
from Tkinter import *  
import Tkinter, Tkconstants, tkFileDialog
import os


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

def image_writer(lat,lon,asset,csv,directory,max_distance):

	csv.write(asset) # writing point of interest to csv

	for root,subdir,files in os.walk(directory):

		#sorting files(images) according their name as os.walk gives list of files(images) in random order this make output csv more readable

		files.sort() 

		for file in files:

			image = piexif.load(os.path.join(root,file))	#loading images
			
			try:	
				#extracting latitude and longitude
				lat_img=degrees(image['GPS'][piexif.GPSIFD.GPSLatitude])
				lon_img=degrees(image['GPS'][piexif.GPSIFD.GPSLongitude])
		
			except KeyError: # evoked when 'GPS' data of image couldn't be read 
				
				lat_img=None
				lon_img=None
				
			if((lat_img and lon_img)  is not None):

				#-------calculating distance b/w every image and drone coordinate at ith second

				if(int(1000*(distance(lat,lon,lat_img,lon_img)))<max_distance):
					
					image_to_write = "" +"," + file 
					
					csv.write(image_to_write) #writing eligible images to output csv
			
					
	csv.write(" "+","+"\n")



def main_exec():

	try:
		
		#---------------------GUI for files(.csv,images folder) selection------------------------------
		
		root = Tk()
			
		root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select csv file",filetypes = (("CSV","*.csv"),("all files","*.*")))		
		#-------- file dialog for file saving-------------------------------
		root.filename2 = tkFileDialog.asksaveasfilename(initialdir = "/",title = "select directory to save ",filetypes = (("CSV file","*.csv"),("all files","*.*")))
		# ------- file dialog for image folder selection-----------------------
		root.directory = tkFileDialog.askdirectory(initialdir="/",title="please select images folder")

		root.destroy()	
		
		# --------------------------------------output csv file creation -------------------------------------
		
		output_csv= open(root.filename2, "a")

		output_csv.write("ASSET"+","+"IMAGES\n")

		distance_radius=raw_input("give the the distance within which images you want  :")
		
		with open(root.filename) as File:  
			
			reader = csv.reader(File) 
			
			for row in reader:
				
				try :		

					image_writer(float(row[2]),float(row[1]),row[0],output_csv,root.directory,int(distance_radius))
				
				except ValueError: #evoked when anyof entry lat,long or input distance is not valid
					continue	
					
		print "file(.csv) saved at  :",root.filename2 #can be changed via gui 
		
	except ValueError: # evoked when no_vids(no of videos) is not a valid entry
		print "please enter an integer next time\n"
		print ".......aborting"

main_exec()
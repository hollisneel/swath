#######################################################
#                                                     #
# Univer,sity of Georgia SmallSat Research Laboratory  #
# Nicholas Neel                                       #
#                                                     #
#######################################################
import math

class camera:
	def __init__( self ,  altitude=400 , object_radius=6371, offsetx = 0 , offsety = 0, field_of_viewx = -1 , field_of_viewy = -1, dist_sensorx = -1, dist_sensory =-1, num_pixelsx = -1, num_pixelsy =-1, focal_length = -1, name = "Default" ):
		
		
		# Is there a more clever way of asking for the above arguments?


		self.__num_total_pixels = num_pixelsx*num_pixelsy
		self.__num_pixels_x = num_pixelsx
		self.__num_pixels_y = num_pixelsy
		self.__sensor_size_x = dist_sensorx
		self.__sensor_size_y = dist_sensory
		self.__altitude = altitude
		self.__radius_of_the_object = object_radius
		self.__offset_x = offsetx
		self.__offset_y = offsety
		self.__field_of_view_x = field_of_viewx
		self.__field_of_view_y = field_of_viewy
		self.__focal_length = focal_length
		self.__name = name

	def swath_sphere(self,string = "x"):
		alt = float(self.__altitude)
		re = float(self.__radius_of_the_object)
		if string == "x":
			fov = float(self.__field_of_view_x)
			off = float(self.__offset_x)
		if string == "y":
			fov = float(self.__field_of_view_y)
			off = float(self.__offset_y)
		ang1 = float(off + (fov/2.))
		ang2 = float(off - (fov/2.))

		omega1 = (math.asin(((alt/re)+1.)*math.sin(ang1*math.pi/180.)) - (ang1)*math.pi/180.)
		omega2 = math.asin(((alt/re)+1.)*math.sin(ang2*math.pi/180.)) - ang2*math.pi/180.
		
		while omega1 > math.pi/2. or omega1 < -math.pi/2.:
		
			if omega1 > math.pi/2.:
				omega1 -= math.pi
			if omega1 < -math.pi/2.:
				omega1 += math.pi
		while omega2 > math.pi/2. or omega2 < -math.pi/2.:
			if omega2 > math.pi/2.:
				omega2 -= math.pi
			if omega2 < -math.pi/2.:
				omega2 += math.pi
		if omega1-omega2 <= 0:
			return -re*(omega1-omega2)
		return re*(omega1-omega2)
	
	def meters_per_pixel(self, string = "x",x=0,y=0):
		if string == "x":
			fov  = float(self.__field_of_view_x)
			angle_pixel = fov/float(self.__num_pixels_x)
			off = float(self.__offset_x)
		if string == "y":
			fov = self.__field_of_view_y
			angle_pixel = fov/float(self.__num_pixels_y)
			off = float(self.__offset_y)
		alt = float(self.__altitude)
		re = float(self.__radius_of_the_object)
		ang1 = float(off + (fov/2.))
		ang2 = float(off - (fov/2.))

		omega1 = (math.asin(((alt/re)+1.)*math.sin((ang2+(x    )*angle_pixel)*math.pi/180.)) - (ang2+(x    )*angle_pixel)*math.pi/180.)
		omega2 = (math.asin(((alt/re)+1.)*math.sin((ang2+(x+1.0)*angle_pixel)*math.pi/180.)) - (ang2+(x+1.0)*angle_pixel)*math.pi/180.)
		
		while omega1 > math.pi/2. or omega1 < -math.pi/2.:
			if omega1 > math.pi/2.:
				omega1 -= math.pi
			if omega1 < -math.pi/2.:
				omega1 += math.pi
		while omega2 > math.pi/2. or omega2 < -math.pi/2.:
			if omega2 > math.pi/2.:
				omega2 -= math.pi
			if omega2 < -math.pi/2.:
				omega2 += math.pi
		if omega1-omega2 <= 0:
			return -re*(omega1-omega2)*1000.0
		return re*(omega1-omega2)*1000.0



	def set_altitude(self,num):
		self.__altitude = num
	def set_object_radius(self,num):
		self.__radius_of_the_object = num
	def set_xz_offset(self,num):
		self.__offset_x = num
	def set_yx_offset(self,num):
		self.__offset_y = num
	def set_xz_field_of_view(self,num):
		self.__field_of_view_x = num
	def set_yz_field_of_view(self,num):
		self.__field_of_view_y = num
	def set_x_pixel(self,num):
		self.__pixel_x = num
	def set_y_pixel(self,num):
		self.__pixel_y = num
	def set_sensor_x_length_mm(self,num):
		self.__sensor_size_x = num
	def set_sensor_y_length_mm(self,num):
		self.__sensor_size_y = num
	def set_num_pixels_x(self,num):
		self.__num_pixels_x = num
	def set_num_pixels_y(self,num):
		self.__num_pixels_y = num
	def set_focal_length(self,num):
		self.__focal_length = num
		self.recalculate_field_of_view()
	def set_name(self,string):
		self.__name = string


	def properties(self):
		return {"focal length":self.__focal_length,"altitude" : self.__altitude,"total_pixels": self.__num_total_pixels,"num_pixels_x":self.__num_pixels_x,"num_pixels_y":self.__num_pixels_y,"sensor_size_x_mm" :self.__sensor_size_x,"sensor_size_y_mm":self.__sensor_size_y,"altitude":self.__altitude,"radius_of_the_object":self.__radius_of_the_object,"camera_offset_x": self.__offset_x,"camera_offset_y":self.__offset_y ,"field_of_view_x": self.__field_of_view_x,"field_of_view_y":self.__field_of_view_y,"name" : self.__name}


	def recalculate_field_of_view(self,v="a"):

		if (v == "a" or v == "x") and self.__sensor_size_x != -1 and self.__focal_length != -1:
			self.__field_of_view_x = 2.0*math.atan(float(self.__sensor_size_x)/(2.0*float(self.__focal_length)))*180/math.pi

		if (v == "a" or v == "y") and  self.__sensor_size_y != -1 and self.__focal_length != -1:
			self.__field_of_view_y =  (2.0*math.atan(float(self.__sensor_size_y)/(2.0*float(self.__focal_length))))*180/math.pi

		if self.__sensor_size_x == -1 or self.__focal_length == -1:
			print "Error : Insufficient Input"
			print "        Need sensor size information and focal length"
			return -1
		return


	def foreign_object_mm(self,object_size_mm = 0,cross_section_mm=(0,0),v="x", object_center_mm = (0,0)):

		if v == "x":
			theta = (self.__field_of_view_x)*math.pi/180
			cross = cross_section_mm[0]
			center = object_center_mm[0]
			off = float(self.__offset_x)
		if v == "y":
			theta = self.__field_of_view_y
			cross = cross_section_mm[1]
			center = object_center_mm[1]
			off = float(self.offset_y)
		alt = float(self.__altitude)
		re = float(self.__radius_of_the_object)
		height = cross/(2*math.tan(theta/2.))

		pt1 = abs(center) + abs(object_size_mm/2.)
		pt2 = abs(center) - abs(object_size_mm/2.)
		
		ang1 = math.atan(pt1/height)
		ang2 = math.atan(pt2/height)
			

		

		ang1 = float(off + ang1)
		ang2 = float(off + ang2)

		omega1 = math.asin(((alt/re)+1.)*math.sin(ang1)) - ang1
		omega2 = math.asin(((alt/re)+1.)*math.sin(ang2)) - ang2
		
		while omega1 > math.pi/2. or omega1 < -math.pi/2.:
		
			if omega1 > math.pi/2.:
				omega1 -= math.pi
			if omega1 < -math.pi/2.:
				omega1 += math.pi
		while omega2 > math.pi/2. or omega2 < -math.pi/2.:
			if omega2 > math.pi/2.:
				omega2 -= math.pi
			if omega2 < -math.pi/2.:
				omega2 += math.pi
		if omega1-omega2 <= 0:
			return -re*(omega1-omega2)
		return re*(omega1-omega2)
	

		


nanocam = camera(650,6371,0,0,-1,-1,6.55,4.92,2048,1536,70,"NanoCam C1U")
nanocam.recalculate_field_of_view()

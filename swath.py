#######################################################
#                                                     #
# University of Georgia SmallSat Research Laboratory  #
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
		''' swath_sphere(self,string) takes a camera object and calculates  swath if possible in the x or y direction '''
		alt = float(self.__altitude)
		re = float(self.__radius_of_the_object)

		if string == "x":
			if self.__field_of_view_x == -1:
				self.recalulate_field_of_view('x')
				if self.field_of_view_x == -1:
					print "insufficient information"
					return 0
			fov = float(self.__field_of_view_x)
			off = float(self.__offset_x)
		if string == "y":
			if self.__field_of_view_y == -1:
				self.recalulate_field_of_view('y')
				if self.field_of_view_y == -1:
					print "insufficient information"
					return 0
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



	# This is currently only accurate for the "center pixel" needs refining.
	def meters_per_pixel(self, string = "x",x=0,y=0):
		if string == "x":
			if x >= self.__num_pixels_x:
				print "Invalid Pixel"
				return 0
			fov  = float(self.__field_of_view_x)
			angle_pixel = fov/float(self.__num_pixels_x)
			off = float(self.__offset_x)
		if string == "y":
			if y >= self.__num_pixels_y:
				print "Invalid Pixel"
				return 0
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


	
	def area_per_pixel(self,x=0,y=0)



	def foreign_lens_object(self,string = "x",obj_radius_mm = 31,obj_center=0,cross_section_mm=31):

		if string == "x":
			fov  = float(self.__field_of_view_x)
			off = float(self.__offset_x)
		if string == "y":
			fov = self.__field_of_view_y
			off = float(self.__offset_y)

		angle_obstr = (math.atan(((float(cross_section_mm)/2.0)*(math.tan(fov/2.))/(2.0*float(obj_radius_mm))))/2.)*180/math.pi
		ang_cent = (math.atan(float(obj_center)/((float(cross_section_mm))/(2.0*math.tan(fov/2.)))))*180/math.pi
		print angle_obstr,ang_cent
		alt = float(self.__altitude)
		re = float(self.__radius_of_the_object)
		ang1 = float((off + angle_obstr)+ang_cent)
		ang2 = float((off - angle_obstr)+ang_cent)


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



	def set_altitue(self,num):
		self.altitude = num
	def set_object_radius(self,num):
		self.radius_of_the_object = num
	def set_xz_offset(self,num):
		self.offset_x = num
	def set_yx_offset(self,num):
		self.offset_y = num
	def set_xz_field_of_view(self,num):
		self.field_of_view_x = num
	def set_yz_field_of_view(self,num):
		self.field_of_view_y = num
	def set_x_pixel(self,num):
		self.pixel_x = num
	def set_y_pixel(self,num):
		self.pixel_y = num
	def set_sensor_x_length_mm(self,num):
		self.sensor_size_x = num
	def set_sensor_y_length_mm(self,num):
		self.sensor_size_y = num
	def set_num_pixels_x(self,num):
		self.num_pixels_x = num
	def set_num_pixels_y(self,num):
		self.num_pixels_y = num
	def set_focal_length(self,num):
		self.focal_length = num
	def set_name(self,string):
		self.name = string
	def properties(self):
		return {"total_pixels": self.__num_total_pixels,"num_pixels_x":self.__num_pixels_x,"num_pixels_y":self.__num_pixels_y,"sensor_size_x_mm" :self.__sensor_size_x,"sensor_size_y_mm":self.__sensor_size_y,"altitude":self.__altitude,"radius_of_the_object":self.__radius_of_the_object,"camera_offset_x": self.__offset_x,"camera_offset_y":self.__offset_y ,"field_of_view_x": self.__field_of_view_x,"field_of_view_y":self.__field_of_view_y,"name" : self.__name}



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


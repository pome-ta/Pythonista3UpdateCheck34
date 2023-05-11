from objc_util import *
from time import sleep
def Country_reverseGeocodeLocation(lat,lon):
	global handler_done,ISOcountryCode
	handler_done = None
	ISOcountryCode = None
	def handler(_cmd,obj1_ptr,_error):
		global handler_done,ISOcountryCode
		print('handler called')
		try:		
			if not _error and obj1_ptr:
				obj1 = ObjCInstance(obj1_ptr)
				for CLPlacemark in obj1:
					ISOcountryCode = str(CLPlacemark.ISOcountryCode())
					if ISOcountryCode == 'None':
						# special case of Market Reef island which belongs to Sweden and Finland,
						# and Apple reverseGeocodeLocation does not return an ISOcountryCode
						# check if location name = Bottenhavet (see of island), simulate
						# returns Finland. Market Reef entity will be identified later
						#print(str(CLPlacemark.name()))
						if str(CLPlacemark.name()) == 'Bottenhavet':
							ISOcountryCode = 'FI'
		except Exception as e:
			print('error',e)
		handler_done = True
		return
		
	CLGeocoder = ObjCClass('CLGeocoder').alloc().init()
	handler_block = ObjCBlock(handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])	
	CLLocation = ObjCClass('CLLocation').alloc().initWithLatitude_longitude_(lat,lon)
	CLGeocoder.reverseGeocodeLocation_completionHandler_(CLLocation, handler_block)	
	# wait handler called and finished
	while not handler_done:
		sleep(0.01)
	return ISOcountryCode
	
lat,lon = (-51.6500051, -58.4924793)
print(Country_reverseGeocodeLocation(lat,lon))

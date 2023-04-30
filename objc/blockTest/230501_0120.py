import photos
from objc_util import ObjCClass, ObjCInstance, ObjCBlock

def download_cloud_asset(asset):
	PHImageManager = ObjCClass('PHImageManager')
	PHImageRequestOptions = ObjCClass('PHImageRequestOptions')
	ph_asset = ObjCInstance(asset)
	ph_image_mgr = PHImageManager.defaultManager()
	req_options = PHImageRequestOptions.alloc().init().autorelease()
	req_options.synchronous = True
	req_options.networkAccessAllowed = True
	def handler_f(*args):
		pass
	handler_block = ObjCBlock(handler_f)
	ph_image_mgr.requestImageDataForAsset(ph_asset, options=req_options, resultHandler=handler_block)

def main():
	a = photos.get_assets()[-1]
	print('Downloading data for last asset... (if needed)')
	download_cloud_asset(a)
	print('Done')

if __name__ == '__main__':
	main()

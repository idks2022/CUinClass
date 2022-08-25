import requests

def get_image_from_url(imgurl):
    resp = requests.get(imgurl)
    imgbytes = resp.content
    return imgbytes

def get_image_from_file(filename):
    with open(filename, 'rb') as imgfile:
            return imgfile.read()
        
        
def get_image(img):
    # Loads and returns the image either from a URL or a file
    if img.lower().startswith('http'):
        return get_image_from_url(img)
    else:
        return get_image_from_file(img)
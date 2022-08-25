from http import client 
import boto3
from pprint import pprint
import image_loaders



# s3 = boto3.resource('s3')

# print(s3.buckets.all())

# for bucket in s3.buckets.all():
#     print(bucket) 
    
    
client = boto3.client('rekognition')

# imgurl = 'https://library.sportingnews.com/styles/crop_style_16_9_mobile/s3/2022-03/shutterstock_1227574510.jpg?h=fc44d7a4&itok=dCfs0FNS'
# imgbytes = image_helpers.get_image_from_url(imgurl)

# rekresp = client.detect_labels(Image={'Bytes': imgbytes})

# pprint(rekresp) 
# print ("Here's what i see:")
# for label in rekresp['Labels']:
#         print(label['Name'])
        

imgfilename = 'D:/CUinClass/CUinClass/cuinclass/core/rekog/images/idan.jpg'
imgbytes = image_loaders.get_image_from_file(imgfilename)

rekresp2 = client.detect_faces(Image={'Bytes': imgbytes},
                               Attributes=['ALL'])

pprint(rekresp2)
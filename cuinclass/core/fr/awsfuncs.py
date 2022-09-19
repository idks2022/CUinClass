import boto3 
# from core.fr.image_loaders import get_image
from botocore.exceptions import ClientError
# from cuinclass.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_REGION
import os
from dotenv import load_dotenv
load_dotenv()

#AWS credentials read from .env file (locally) or environment variables when deployed on server
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')

client=boto3.client('rekognition',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION)

def create_collection(collection_id):
    # client=boto3.client('rekognition') //line16

    #Create a collection
    print('Creating collection:' + collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')
    

def list_collections():
    # client=boto3.client('rekognition') //line16
    max_results=2

    #Display all the collections
    print('Displaying collections...')
    response=client.list_collections(MaxResults=max_results)
    collection_count=0
    done=False
    
    while done==False:
        collections=response['CollectionIds']

        for collection in collections:
            print (collection)
            collection_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_collections(NextToken=nextToken,MaxResults=max_results)
            
        else:
            done=True
    #return collection_count 
    print("collections: " + str(collection_count))


def describe_collection(collection_id):

    print('Attempting to describe collection ' + collection_id)
    # client=boto3.client('rekognition') //line16

    try:
        response=client.describe_collection(CollectionId=collection_id)
        print("Collection Arn: "  + response['CollectionARN'])
        print("Face Count: "  + str(response['FaceCount']))
        print("Face Model Version: "  + response['FaceModelVersion'])
        print("Timestamp: "  + str(response['CreationTimestamp']))

        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collection_id + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
    print('Done...')


def delete_collection(collection_id):


    print('Attempting to delete collection ' + collection_id)
    # client=boto3.client('rekognition') //line16
    status_code=0
    try:
        response=client.delete_collection(CollectionId=collection_id)
        status_code=response['StatusCode']
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collection_id + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
        status_code=e.response['ResponseMetadata']['HTTPStatusCode']
    # return(status_code)
    print('Status code: ' + str(status_code))

#from outside s3 bucket
# def add_faces_to_collection(image,collection_id): 

#     def extract_filename(fname_or_url: str) -> str:
#         import re
#         return re.split('[\\\/]', fname_or_url)[-1]
    
#     # client=boto3.client('rekognition') //line16

#     response=client.index_faces(CollectionId=collection_id,
#                                 Image={'Bytes': get_image(image)},
#                                 ExternalImageId=extract_filename(image) ,
#                                 MaxFaces=1,
#                                 QualityFilter="AUTO",
#                                 DetectionAttributes=['ALL'])

#     print ('Results for ' + image) 	
#     print('Faces indexed:')						
#     for faceRecord in response['FaceRecords']:
#          print('  Face ID: ' + faceRecord['Face']['FaceId'])
#          print('  External Image Id: ' + faceRecord['Face']['ExternalImageId'])
#          print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

#     print('Faces not indexed:')
#     for unindexedFace in response['UnindexedFaces']:
#         print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
#         print(' Reasons:')
#         for reason in unindexedFace['Reasons']:
#             print('   ' + reason)
#     # print("Faces indexed count: " + str('FaceRecords'))
#     # return len(response['FaceRecords'])

#from s3 bucket
def add_faces_to_collection(bucket,photo,name,collection_id):
    
    # client=boto3.client('rekognition')//line15

    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=name,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo) 	
    print('Faces indexed:')						
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  External Image Id: ' + faceRecord['Face']['ExternalImageId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])


def list_faces_in_collection(collection_id):
    
    maxResults=20
    faces_count=0
    tokens=True

    # client=boto3.client('rekognition') //line16
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)

    print('Faces in collection ' + collection_id)

 
    while tokens:

        faces=response['Faces']

        for face in faces:
            print (face)
            faces_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False
    return faces_count   


def delete_faces_from_collection(collection_id, faces):

    # client=boto3.client('rekognition') //line16

    response=client.delete_faces(CollectionId=collection_id,
                               FaceIds=faces)
    
    print(str(len(response['DeletedFaces'])) + ' faces deleted:') 							
    for faceId in response['DeletedFaces']:
         print (faceId)
    return len(response['DeletedFaces'])


def find_face(collection_id, image):

    print('Searching for face match...')
    #client=boto3.client('rekognition') //line16
    
    response=client.search_faces_by_image(CollectionId=collection_id,
                                Image={'Bytes': get_image(image)},
                                FaceMatchThreshold=70,
                                MaxFaces=1)

                                
    faceMatches=response['FaceMatches']
    result = 'Matching faces: '
    if len(faceMatches) > 0:
        for match in faceMatches:
            print(result)
            print ('FaceId:' + match['Face']['FaceId'])
            print ('FaceName:' + match['Face']['ExternalImageId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            return (match['Face']['ExternalImageId'])
    else:
        result += 'There is no match'
        print(result)
    


def main():
    # create_collection('students')
    list_collections()
    # describe_collection('students')
    # delete_collection('studentsCollection')
    # upload_image('cuinclass/core/fr/facesToCollection/Idan.jpg')
    
    # add_faces_to_collection(Gal,'students')
    # add_faces_to_collection('custudents','Rey_Hadas.jpg','students')

    # imageToScan = 'cuinclass/core/fr/imagesToScan/sarah.jpg'
    # find_face('students', imageToScan)
    
    faces_count=list_faces_in_collection('students')
    print("faces count: " + str(faces_count))
    
    # faces=[]
    # faces.append("843fe7fa-5a8e-429e-a5e4-2840d9af332f")
    # faces_count=delete_faces_from_collection('students', faces)
    # print("deleted faces count: " + str(faces_count))

if __name__ == "__main__":
    main()
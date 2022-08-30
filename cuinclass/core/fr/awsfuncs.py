import boto3 
from pathlib import Path
from pprint import pprint
from core.fr.image_loaders import get_image
from typing import List
from botocore.exceptions import ClientError
from os import environ


def create_collection(collection_id):
    client=boto3.client('rekognition')

    #Create a collection
    print('Creating collection:' + collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')
    

def list_collections():

    max_results=2
    
    client=boto3.client('rekognition')

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
    client=boto3.client('rekognition')

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
    client=boto3.client('rekognition')
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

 
def add_faces_to_collection(bucket,image,collection_id):

    def extract_filename(fname_or_url: str) -> str:
        import re
        return re.split('[\\\/]', fname_or_url)[-1]
    
    client=boto3.client('rekognition')

    response=client.index_faces(CollectionId=collection_id,
                                Image={'Bytes': get_image(image)},
                                ExternalImageId=extract_filename(image) ,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + image) 	
    print('Faces indexed:')						
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    print("Faces indexed count: " + str('FaceRecords'))
    # return len(response['FaceRecords'])

def find_face(collection_id, image):

    print('Searching for face match...')
    client=boto3.client('rekognition')
    
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
    else:
        result += 'There is no match'
        print(result)


def main():
    # create_collection('students')
    # list_collections()
    # describe_collection('students')
    # delete_collection('studentsCollection')
    # upload_image('cuinclass/core/fr/facesToCollection/Idan.jpg')
    
    # Gal = 'cuinclass/core/fr/facesToCollection/Gal.jpg'
    # Idan = 'cuinclass/core/fr/facesToCollection/idan.jpg'
    # Rey = 'cuinclass/core/fr/facesToCollection/Rey.jpg'
    # add_faces_to_collection('cuinclass',Rey,'students')

    # imageToScan = 'cuinclass/core/fr/imagesToScan/sarah.jpg'
    # find_face('students', imageToScan)

if __name__ == "__main__":
    main()
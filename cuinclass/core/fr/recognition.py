from pickle import TRUE
import boto3
import csv

# def get_rekognition_connection():
#     #get aws rekognition connection
#     with open('cuinclass/core/fr/credentials.csv', 'r') as input:
#         next(input)
#         reader = csv.reader(input)
#         for line in reader:
#             access_key_id = line[0]
#             secret_access_key = line[1] 
#     # # print to check credentials have been copied     
#     #     print(access_key_id)
#     #     print(secret_access_key)

    # client = boto3.client('rekognition',
    #                         aws_access_key_id = access_key_id,
    #                         aws_secret_access_key = secret_access_key,
    #                         )
    # return client

def upload_image(image='cuinclass/core/fr/input.jpg'):
    s3 = boto3.resource('s3')
    # Upload input image to bucket
    data = open(image, 'rb')
    s3.Bucket('custudents').put_object(Key='input.jpg', Body=data)
    return True

#compare face from input image to faces in the collection
if __name__ == "__main__":

    upload_image()

    bucket='custudents'
    collectionId='studentsCollection'
    fileName='input.jpg'
    threshold = 70
    maxFaces=2

    client=boto3.client('rekognition')
    response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)

                                
    faceMatches=response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print


# # Let's use Amazon S3
# s3 = boto3.resource('s3')

# # Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)

# # Upload a new file
# data = open('cuinclass/core/fr/test.jpg', 'rb')
# s3.Bucket('custudents').put_object(Key='test.jpg', Body=data)   

# # Get the service resource
# sqs = boto3.resource('sqs')

# # Create the queue. This returns an SQS.Queue instance
# queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

# # You can now access identifiers and attributes
# print(queue.url)
# print(queue.attributes.get('DelaySeconds'))
import boto3
import json
import collections
from boto3.dynamodb.conditions import Key, Attr

print('Loading function')
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

def getRawzoneData(pdsuser):

    recList = collections.defaultdict(list)
    #reclist['finance'] =[]
    #reclist['shopping'] =[]
    #reclist['travel'] =[]
    test_table = dynamodb.Table('PDS_Meta_RawZone')
    # Give me all items where primary key "column1" = "fruit1"
    response = test_table.scan(
        FilterExpression=Attr('userid').eq(pdsuser)
    )
    for item in response['Items']:
        respItem={}
        url = s3_client.generate_presigned_url('get_object',Params={'Bucket': item['bucket'],'Key': item['resource']},ExpiresIn=7200)
        respItem['name'] = item['resource'].split('/')[3]
        respItem['url'] = url
        recList[item['catogery']].append(respItem)
    
    return recList;

def lambda_handler(event, context):

    body=json.loads(event['body'].replace("\n",""))
    print("=========================================")
    #print("Received event: " + str(body))
    print("Received parameter: " + body['username'])
    print("=========================================")
    
    userTable = dynamodb.Table('PDS_UserProfile')
    userTabResponse = userTable.get_item(Key={'username': body['username']})
    pdsuser = userTabResponse['Item']['userid']

    responseBody =getRawzoneData(pdsuser)

    print("============RESP BODY===============")
    print(json.dumps(responseBody))
    print("============END===============")
    return {
        'statusCode': 200,
        'headers': {
          'Access-Control-Allow-Origin': "*",
          'Access-Control-Allow-Headers': 'x-requested-with'
        },
        'body': json.dumps(responseBody)
    }


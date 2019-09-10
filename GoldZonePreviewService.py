import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

print('Loading function')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    body=json.loads(event['body'].replace("\n",""))
    print("=========================================")
    #print("Received event: " + str(body))
    print("Received parameter: " + body['username'])
    print("=========================================")

    test_table = dynamodb.Table('PDS_GZ_FinanceData')
    # Give me all items where primary key "column1" = "fruit1"
    response = test_table.scan(
        FilterExpression=Attr('user').eq('dfdhjk37ghhzx57')
    )
    #response = table.query(
    #    KeyConditionExpression=Key('user').eq('dfdhjk37ghhzx57')
    #)
    responseBody ={}
    responseBody['count'] = len(response['Items'])
    responseBody['transactions'] = [response['Items'][0],response['Items'][1],response['Items'][2]]
    print("===========================")
    print("Total no of items : "+ str(len(response['Items'])))
    print(json.dumps(responseBody))
    print("===========================")
    return {
        'statusCode': 200,
        'headers': {
          'Access-Control-Allow-Origin': "*",
          'Access-Control-Allow-Headers': 'x-requested-with'
        },
        'body': json.dumps(responseBody)
    }


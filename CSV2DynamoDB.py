import json
import csv
import boto3


def lambda_handler(event, context):
    
    region = 'us-west-1'
    record_list = []
    
    #bucket and csv file are the "event"
    try:
        s3 = boto3.client('s3')
        
        dynamodb = boto3.client('dynamodb', region_name = region)
        
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event ['Records'][0]['s3']['object']['key']
        print('Bucket:', bucket, ' Key:', key)
    
        csv_file = s3.get_object(Bucket = bucket, Key = key)
        
        record_list = csv_file['Body'].read().decode('utf-8').split('\n')
        
        csv_reader = csv.reader(record_list, delimiter = ',', quotechar = '"')
    
        for row in csv_reader:
            pick_order_number = row[0]
            champion = row[1]
            role = row[2]
            damage_type = row[3]
            position = row[4]
            gold_in_thousands = row[5]
            print(f'Order: {pick_order_number:2s}    Champion: {champion:7s}    Role: {role:12s}    Damage Type: {damage_type:2s}    Position: {position:3s}    Gold: {gold_in_thousands:3s}')
            
            add_to_db = dynamodb.put_item(
                TableName = 'League_Team',
                Item = {
                    'pick_order_number' : {'N': str(pick_order_number)},
                    'champion' : {'S': str(champion)},
                    'role' : {'S': str(role)},
                    'damage_type' : {'S': str(damage_type)},
                    'position' : {'S': str(position)},
                    'gold_in_thousands' : {'N': str(gold_in_thousands)},
                })
            print('DynamoDB upload success!!!')
            
    except Exception as e:
        print(str(e))
            
            
    return {
        'statusCode': 200,
        'body': json.dumps('CSV to DynamoDB Success')
    }

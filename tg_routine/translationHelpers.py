from asgiref.sync import async_to_sync

from main import *


@async_to_sync
async def retrieve_labels():
    print('retrieve_labels')
    response = dynamodb_client.scan(TableName=secrets['DYNAMO_DB_TRANSLATIONS'])

    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = dynamodb_client.scan(TableName=secrets['DYNAMO_DB_TRANSLATIONS'],
                                        ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    labels = parse_translations_list(items)
    for label in labels:
        labels_cache[label] = labels[label]

    return labels


def get_remote_label(label: str, language: str):
    print('get_remote_label')
    data = dynamodb_client.get_item(
        TableName=secrets['DYNAMO_DB_TRANSLATIONS'],
        Key={
            'label': {
                'S': label
            }
        }
    )
    if not 'Item' in data:
        raise Exception(f'No translation provided for: {label}')

    translations = data['Item']['language']['M']
    if not language in translations:
        raise Exception(f'No {language} translation provided for: {label}')

    return translations[language]['S']


def parse_translations_list(lst):
    result = {item['label']['S']: {k: v['S'] for k, v in item['language']['M'].items()} for item in lst}
    return result


def get_label(label: str, language: str):
    print('get_label')
    print(labels_cache)
    if label not in labels_cache or language not in labels_cache[label]:
        print(label not in labels_cache)
        print(label not in labels_cache or language not in labels_cache[label])
        return get_remote_label(label, language)

    return labels_cache[label][language]

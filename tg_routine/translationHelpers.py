from main import *


def retrieve_labels():
    response = dynamodb_client.scan(TableName=secrets['DYNAMO_DB_TRANSLATIONS'])

    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = dynamodb_client.scan(TableName=secrets['DYNAMO_DB_TRANSLATIONS'],
                                        ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return parse_translations_list(items)


def get_remote_label(label: str, language: str):
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
    if label not in labels_cache or language not in labels_cache[label]:
        return get_remote_label(label, language)

    return labels_cache[label][language]

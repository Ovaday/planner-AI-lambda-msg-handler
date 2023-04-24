from main import secrets, dynamodb_client


def get_label(label: str, language: str):
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

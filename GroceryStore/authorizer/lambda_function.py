import json


def generate_policy(principal_id, effect, resource, context=None):
    auth_response = {'principalId': principal_id}

    if effect and resource:
        policy_document = {'Version': '2012-10-17',
                           'Statement': [{'Action': 'execute-api:Invoke', 'Effect': effect, 'Resource': resource}]}
        auth_response['policyDocument'] = policy_document

    if context is None:
        context = {}

    auth_response['context'] = context

    return json.dumps(auth_response)


def lambda_handler(event, context):
    token = event['authorizationToken']

    response = None
    if token == 'aaaaaaaa':
        response = generate_policy('user', 'Allow', event['methodArn'],
                                   {
                                       'email': 'aaronroh.public@gmail.com',
                                       'full_name': '노아론1'
                                   })
    elif token == 'bbbbbbbb':
        response = generate_policy('user', 'Allow', event['methodArn'],
                                   {
                                       'email': 'roharon98@gmail.com',
                                       'full_name': '노아론2'
                                   })

    return json.loads(response) if response is not None else 'unauthorized'

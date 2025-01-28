def user_schema(user) -> dict:
    return {
        'id': str(user['_id']),
        'fullname': user['fullname'],
        'alias': user['alias'],
        'age': user['age']
    }
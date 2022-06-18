def exception_data(view):
    try:
        data = view.exception_data
    except Exception as e:
        data = {}
    response = {
        'status': data.get('status', 500),
        'message': data.get('message', ''),
        'data': data.get('data', None),
        'extra': data.get('extra', None),
        'paginate': data.get('pagination', None)
    }
    return response, data

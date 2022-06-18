def log_data(view):
    try:
        path = view.__class__.__name__
    except Exception as e:
        path = 'NONE'
    try:
        logger = view.logger
    except Exception as e:
        logger = None
    try:
        version = view.version
    except Exception as e:
        version = None

    return path, logger, version

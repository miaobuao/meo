'''
    function may be used in flask app.
'''
def allow_cors(flask_app):
    """
        allow cors after requet.
    """
    @flask_app.after_request
    def cors(environ):
        environ.headers['Access-Control-Allow-Origin'] = '*'
        environ.headers['Access-Control-Allow-Method'] = '*'
        environ.headers["Access-Control-Allow-Credentials"] = 'true'
        environ.headers['Access-Control-Allow-Headers'] = 'Content-Type, Depth, User-Agent, " \
            "X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control'
        return environ

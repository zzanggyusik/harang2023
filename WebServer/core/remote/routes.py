from .views import (
    show_remote, belt_detail,
    remote_start, remote_stop,
    request_xray_data
)
    

def initialize_routes(remote):
    remote.add_url_rule('/', view_func=show_remote, methods=['GET'])
    remote.add_url_rule('/detail/<belt_id>', view_func=belt_detail, methods=['GET'])
    remote.add_url_rule('/detail/<belt_id>/start', view_func=remote_start, methods=['GET'])
    remote.add_url_rule('/detail/<belt_id>/stop', view_func=remote_stop, methods=['GET'])
    remote.add_url_rule('/detail/<belt_id>/request_xray_data', view_func=request_xray_data, methods=['POST'])

from .views import (
    login_user, logout_user,
    register_user, check_id
)

def initialize_routes(login, register): #mypage 추가
    login.add_url_rule('/', view_func=login_user, methods=['GET', 'POST'])
    login.add_url_rule('/logout', view_func=logout_user)
    register.add_url_rule('/', view_func=register_user, methods=['GET', 'POST'])
    register.add_url_rule('/check_id', view_func=check_id, methods=['POST'])

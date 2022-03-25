from flask import jsonify
from api import db
from api import admin
from api.auth import basic_auth



@admin.route('/tokens')
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.sesssion.commit()
    return jsonify({'token': token})

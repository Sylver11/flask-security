from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, redirect, url_for, request, current_app, jsonify

class SecurityManager__Views(object):

    def login_view(self):
        if current_user.is_authenticated:
            return redirect(url_for('home_bp.index'))
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = self._datastore.get_user_by_email(email)
            number = 5 / 0
            if not user:
                current_app.logger.info('%s does not exist', email)
                return jsonify({
                    'status': 401,
                    'redirect': False,
                    'address': None,
                    'message': 'Incorrect Email or Password',
                    'model': None
                    })
            if user.check_password(password):
                login_user(user)
                user.authenticated = True
                self._datastore.update_user(user)
                return jsonify({
                    'status': 200,
                    'redirect': True,
                    'address': '/',
                    'message': 'Successully logged in',
                    'model': None
                    })
            else:
                current_app.logger.info('%s failed to log in', email)
                return jsonify({
                    'status': 401,
                    'redirect': False,
                    'address': None,
                    'message': 'Incorrect Email or Password',
                    'model': None
                    })
        return render_template(self.FLASK_SECURITY_LOGIN_TEMPLATE)

    def logout_view(self):
        current_user.authenticated = False
        self._datastore.update_user(current_user)
        logout_user()
        return redirect(self.FLASK_SECURITY_AFTER_LOGOUT_URL)

#    @catch_view_exception
#    def register_view(self):
#        if current_user.is_authenticated:
#            return redirect(url_for('home_bp.index'))
#        if request.method == 'POST':
#            new_user = User(request.form)
#            new_user = self.user_datastore.add_user(new_user, request.form['password'])
#            if isinstance(new_user, User):
#                if new_user.uuid:
#                    return self._json_response(True,'/','')
#                return self._json_response(False,'','Could not create user')
#            return self._json_response(False,'','User already exists')
#        return render_template(self.USER_REGISTER_TEMPLATE)
#
    def test_view(self):
        return 'Success'


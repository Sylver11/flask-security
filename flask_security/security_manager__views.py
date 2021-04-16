from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, redirect, url_for, request, current_app
from .decorators import catch_view_exception

class SecurityManager__Views(object):

    @catch_view_exception
    def login_view(self):
        if current_user.is_authenticated:
            return redirect(url_for('home_bp.index'))
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = self.user_datastore.get_user_by_email(email)
            if not user:
                current_app.logger.info('%s does not exist', email)
                return 'User does not exist'
            if user.check_password(password):
                login_user(user)
                user.authenticated = True
                self.user_datastore.update_user(user)
                return redirect(url_for('home_bp.index'))
            else:
                current_app.logger.info('%s failed to log in', email)
                return 'Password is incorrect'
        return render_template(self.FLASK_SECURITY_LOGIN_TEMPLATE)

    @catch_view_exception
    def logout_view(self):
        current_user.authenticated = False
        self.user_datastore.update_user(current_user)
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


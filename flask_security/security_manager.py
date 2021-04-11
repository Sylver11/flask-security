from flask_login import LoginManager
from flask import Blueprint
from .security_manager__settings import SecurityManager__Settings
from .security_manager__views import SecurityManager__Views
from .security_manager__utils import SecurityManager__Utils

class SecurityManager(SecurityManager__Settings,
        SecurityManager__Views,
        SecurityManager__Utils):

    def __init__(self, app=None, user_datastore=None):
        self.app = app
        self.user_datastore = user_datastore
        if app:
            self.init_security(app)

    def init_security(self, app):
        app.manager = self
        self.login_manager = LoginManager(app)
        self.login_manager.login_view = 'flask_security_bp.login'
        @self.login_manager.user_loader
        def load_user(uuid):
            return self.user_datastore.get_user_by_uuid(uuid)

        flask_security = Blueprint(
                'flask_security_bp',
                __name__,
                template_folder='templates',
                static_folder='static',)

        app.register_blueprint(flask_security)

        self._add_url_routes(app)

        from .cli import security_cli
        app.cli.add_command(security_cli)

        #if self.USER_SET_DB_DEFAULTS:
#            role_name = self.USER_DEFAULT_ROLE_NAME
#            role_description = self.USER_DEFAULT_ROLE_DESCRIPTION
#
#            @app.before_request
#            def check_security_db_defaults():
#                role = Role.query.filter_by(name=role_name).first()
#                if not role:
#                    role = Role(name=role_name, description=role_description)
#                    db.session.add(role)
#                self.db.session.commit()

    def _add_url_routes(self, app):

        def test_stub():
            return self.test_view()

        def login_stub():
            return self.login_view()

        def logout_stub():
            return self.logout_view()

        def register_stub():
            if not self.FLASK_SECURITY_ENABLE_REGISTER: abort(404)
            return self.register_view()


        app.add_url_rule(self.FLASK_SECURITY_TEST_URL, 'flask_security_bp.test', test_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.FLASK_SECURITY_REGISTER_URL, 'flask_security_bp.register', register_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.FLASK_SECURITY_LOGOUT_URL, 'flask_security_bp.logout', logout_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.FLASK_SECURITY_LOGIN_URL, 'flask_security_bp.login', login_stub, methods=['GET', 'POST'])

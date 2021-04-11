class SecurityManager__Settings(object):

    FLASK_SECURITY_ENABLE_REGISTER = False
    FLASK_SECURITY_SET_DB_DEFAULTS = True
    FLASK_SECURITY_DEFAULT_ROLE_NAME = 'user'
    FLASK_SECURITY_DEFAULT_ROLE_DESCRIPTION = 'Normal User'
    FLASK_SECURITY_TEST_URL = '/security/test'
    FLASK_SECURITY_LOGIN_URL = '/login'
    FLASK_SECURITY_LOGOUT_URL = '/logout'
    FLASK_SECURITY_REGISTER_URL = '/register'
    FLASK_SECURITY_LOGIN_TEMPLATE = 'flask_security/login.html' #:
    FLASK_SECURITY_REGISTER_TEMPLATE = 'flask_security/register.html' #:
    FLASK_SECURITY_FORGOT_PASSWORD_TEMPLATE = 'flask_security/forgot_password.html' #:
    FLASK_SECURITY_CONFIRM_EMAIL_TEMPLATE = 'flask_security/emails/confirm_email' #:
    FLASK_SECURITY_AFTER_LOGOUT_URL = '/'

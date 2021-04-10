__version__ = '1.0.0'
__author__ = 'Justus Voigt'
__email__ = 'connectmaeuse@gmail.com'

from flask_login import current_user
from .datastore import UserDatastore
from .security_manager import SecurityManager
from .decorators import *

from flask import jsonify, current_app, has_request_context, request
from flask_login import current_user
from werkzeug.exceptions import Forbidden
import sys, traceback
import functools
import logging



def catch_view_exception(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as ex:
            template = 'User uuid:{}\nIP:{}\nRequested URL:{}\nTraceback:{}'
            request_remote_addr = request_url = user_uuid = 'Unknown'
            post = False
            if has_request_context():
                request_url = request.url
                request_remote_addr = request.remote_addr
                if request.method == 'POST':
                    post = True
                if current_user.is_authenticated:
                    user_uuid = current_user.uuid
            admin_error_message = template.format(
                    user_uuid,
                    request_remote_addr,
                    request_url,
                    traceback.format_exc())
            current_app.logger.error(admin_error_message)
            template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
            user_error_message = template.format(type(ex).__name__, ex.args)
            if post:
                return jsonify(user_error_message), 500
            return user_error_message
    return inner


def import_user():
    try:
        from flask_login import current_user
        return current_user
    except ImportError:
        raise ImportError(
            'User argument not passed and Flask-Login current_user could not be imported.')


def ability_required(ability, get_user=import_user):
    """
    Takes an ability (a string name of either a role or an ability) and returns the function if the user has that ability
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            from .models import Ability
            desired_ability = Ability.query.filter_by(name=ability).first()
            user_abilities = []
            current_user = get_user()
            for role in current_user.roles:
                user_abilities += role.abilities
            if desired_ability in user_abilities:
                return func(*args, **kwargs)
            else:
                raise Forbidden("You do not have access")
        return inner
    return wrapper


def role_required(role, get_user=import_user):
    """
    Takes an role (a string name of either a role or an ability) and returns the function if the user has that role
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            from .models import Role
            current_user = get_user()
            if role in current_user.roles:
                return func(*args, **kwargs)
            raise Forbidden("You do not have access")
        return inner
    return wrapper

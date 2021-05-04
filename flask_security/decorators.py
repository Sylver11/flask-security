from werkzeug.exceptions import Forbidden
from flask_security import current_user
import functools


def role_required(role: str):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            user_roles = [role.name for role in current_user.roles]
            if role in user_roles:
                return func(*args, **kwargs)
            raise Forbidden("You do not have access")
        return inner
    return wrapper


def roles_required(roles: dict):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            user_roles = [role.name for role in current_user.roles]
            if roles.issubset(user_roles):
                return func(*args, **kwargs)
            raise Forbidden("You do not have access")
        return inner
    return wrapper


def roles_optional(roles: dict):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            user_roles = [role.name for role in current_user.roles]
            for role in roles:
                if role in user_roles:
                    return func(*args, **kwargs)
            raise Forbidden("You do not have access")
        return inner
    return wrapper


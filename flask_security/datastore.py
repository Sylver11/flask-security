from flask import current_app
#from .models import User, Group, Role


class Datastore:
    def __init__(self, db):
        self.db = db

    def commit(self):
        from sqlalchemy.exc import IntegrityError
        from sqlalchemy.exc import SQLAlchemyError
        try:
            return self.db.session.commit()
        except IntegrityError as err:
            self.db.session.rollback()
            current_app.logger.info(err)
            return 'Integrity Error: The relational integrity of the database could be adversely affected by this operation.'
        except SQLAlchemyError as err:
            self.db.session.rollback()
            current_app.logger.error(err)
            return 'Fatal database error: Server Admin was informed'
#        finally:
#            self.db.session.close()

    def put(self, model):
        self.db.session.add(model)

    def update(self, model):
        self.db.session.merge(model)

    def delete(self, model):
        self.db.session.delete(model)


class UserDatastore(Datastore):

    def __init__(self, db, user_model, group_model, role_model):
        Datastore.__init__(self, db)
        self.user_model = user_model
        self.group_model = group_model
        self.role_model = role_model

#    def _prepare_role_modify_args(self, role):
#        if isinstance(role, str):
#            role = self.find_role(role)
#        return role
#
#    def _prepare_create_user_args(self, **kwargs):
#        kwargs.setdefault("active", True)
#        roles = kwargs.get("roles", [])
#        for i, role in enumerate(roles):
#            rn = role.name if isinstance(role, self.role_model) else role
#            # see if the role exists
#            roles[i] = self.find_role(rn)
#        kwargs["roles"] = roles
#        kwargs.setdefault("fs_uniquifier", uuid.uuid4().hex)
#        if hasattr(self.user_model, "fs_token_uniquifier"):
#            kwargs.setdefault("fs_token_uniquifier", uuid.uuid4().hex)
#
#        return kwargs

#    def find_user(self, case_insensitive=False, **kwargs):
#        from sqlalchemy import func as alchemyFn
#
#        query = self.user_model.query
#        if config_value("JOIN_USER_ROLES") and hasattr(self.user_model, "roles"):
#            from sqlalchemy.orm import joinedload
#
#            query = query.options(joinedload("roles"))
#
#        if case_insensitive:
#            # While it is of course possible to pass in multiple keys to filter on
#            # that isn't the normal use case. If caller asks for case_insensitive
#            # AND gives multiple keys - throw an error.
#            if len(kwargs) > 1:
#                raise ValueError("Case insensitive option only supports single key")
#            attr, identifier = kwargs.popitem()
#            subquery = alchemyFn.lower(
#                getattr(self.user_model, attr)
#            ) == alchemyFn.lower(identifier)
#            return query.filter(subquery).first()
#        else:
#            return query.filter_by(**kwargs).first()
    def get_user_by_uuid(self, uuid):
        return self.user_model.query.filter_by(uuid=uuid).first()
        #return user

    def get_user_by_email(self, email):
        return self.user_model.query.filter_by(email=email).first()

    def get_group_by_name(self, name):
        return self.group_model.query.filter_by(name=name).first()
        #return group

#    def user_part_of_default_group(self, user_model):
#        name = self.USER_DEFAULT_GROUP_NAME
#        default_group = self.get_group_by_name(name)
#        if not default_group:
#            return False
#        if default_group.uuid == user_model.group_uuid:
#            return True
#        return False


    def add_user(self, user_model):
        self.put(user_model)
        feedback = self.commit()
        if feedback is None:
            return user_model
        return feedback

    def update_user(self, user_model):
        self.update(user_model)
        feedback = self.commit()
        if feedback is None:
            return user_model
        return feedback

    def delete_user(self, user):
        self.delete(user)
        return self.commit(user)

    def add_group(self, group_model):
        self.put(group_model)
        feedback = self.commit()
        if feedback is None:
            return group_model
        return feedback

    def update_group(self, group_model):
        self.update(group_model)
        feedback = self.commit()
        if feedback is None:
            return group_model
        return feedback

    def delete_group(self, group_model):
        self.delete(group_model)
        return self.commit()

    def find_role(self, role):
        return self.role_model.query.filter_by(name=role).first()


#    def add_role_to_user(self, user, role):
#        role = self._prepare_role_modify_args(role)
#        if role not in user.roles:
#            user.roles.append(role)
#            self.put(user)
#            return True
#        return False
#
#    def remove_role_from_user(self, user, role):
#        rv = False
#        role = self._prepare_role_modify_args(role)
#        if role in user.roles:
#            rv = True
#            user.roles.remove(role)
#            self.put(user)
#        return rv
#
#    def add_permissions_to_role(self, role, permissions):
#        rv = False
#        role = self._prepare_role_modify_args(role)
#        if role:
#            rv = True
#            role.add_permissions(permissions)
#            self.put(role)
#        return rv
#
#    def remove_permissions_from_role(self, role, permissions):
#        rv = False
#        role = self._prepare_role_modify_args(role)
#        if role:
#            rv = True
#            role.remove_permissions(permissions)
#            self.put(role)
#        return rv
#
#    def toggle_active(self, user):
#        user.active = not user.active
#        self.put(user)
#        return True
#
#    def deactivate_user(self, user):
#        if user.active:
#            user.active = False
#            self.put(user)
#            return True
#        return False
#
#    def activate_user(self, user):
#        """Activates a specified user. Returns `True` if a change was made.
#
#        :param user: The user to activate
#        """
#        if not user.active:
#            user.active = True
#            self.put(user)
#            return True
#        return False
#
#
#
#    def create_role(self, **kwargs):
#        if "permissions" in kwargs and hasattr(self.role_model, "permissions"):
#            perms = kwargs["permissions"]
#            if isinstance(perms, list) or isinstance(perms, set):
#                perms = ",".join(perms)
#            elif isinstance(perms, str):
#                # squash spaces.
#                perms = ",".join([p.strip() for p in perms.split(",")])
#            kwargs["permissions"] = perms
#
#        role = self.role_model(**kwargs)
#        return self.put(role)
#
#    def find_or_create_role(self, name, **kwargs):
#        """Returns a role matching the given name or creates it with any
#        additionally provided parameters.
#        """
#        kwargs["name"] = name
#        return self.find_role(name) or self.create_role(**kwargs)
#
#    def create_user(self, **kwargs):
#        kwargs = self._prepare_create_user_args(**kwargs)
#        user = self.user_model(**kwargs)
#        return self.put(user)
#
#    def delete_user(self, user):
#        self.delete(user)
#
#    def reset_user_access(self, user):
#        self.set_uniquifier(user)
#        self.set_token_uniquifier(user)
#        if hasattr(user, "us_totp_secrets"):
#            self.us_reset(user)
#        if hasattr(user, "tf_primary_method"):
#            self.tf_reset(user)
#

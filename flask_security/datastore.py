class Datastore:
    def __init__(self, db):
        self.db = db

    def _put(self, model):
        self.db.session.add(model)

    def _update(self, model):
        self.db.session.merge(model)

    def _delete(self, model):
        self.db.session.delete(model)

    def _commit(self):
        from flask import current_app
        from sqlalchemy.exc import IntegrityError
        from sqlalchemy.exc import SQLAlchemyError
        try:
            self.db.session.commit()
            return True, 'Success'
        except IntegrityError as err:
            self.db.session.rollback()
            current_app.logger.warning(err)
            return False, err
        except SQLAlchemyError as err:
            self.db.session.rollback()
            current_app.logger.error(err)
            return False, err
        return False, 'Unkown error occured'


    def _commit_and_update_model(self, model):
        status, response = self._commit()
        model.query_status = status
        model.query_response = response
        return model

    def add_model(self, model):
        self._put(model)
        model.query_type = 'insert'
        return self._commit_and_update_model(model)

    def update_model(self, model):
        self._update(model)
        model.query_type = 'update'
        return self._commit_and_update_model(model)

    def delete_model(self, model):
        self._delete(model)
        model.query_type = 'delete'
        return self._commit_and_update_model(model)


class UserDatastore(Datastore):
    User = None
    Group = None
    Role = None

    def __init__(self, db, user_model, group_model, role_model):
        Datastore.__init__(self, db)
        self.User = user_model
        self.Group = group_model
        self.Role = role_model

    def get_user_by_uuid(self, uuid: str):
        return self.User.query.filter_by(uuid=uuid).first()

    def get_user_by_email(self, email: str):
        return self.User.query.filter_by(email=email).first()

    def get_users(self):
        return self.User.query.all()

    def add_user_by_model(self, model: User) -> User:
        return self.add_model(model)

    def update_user_by_model(self, model: User) -> User:
        return self.update_model(model)

    def delete_user_by_email(self, email: str) -> User:
        model = self.get_user_by_email(email)
        return self.delete_model(model)

    def delete_user_by_model(self, model: User) -> User:
        return self.delete_model(model)

    def get_group_by_name(self, name: str):
        return self.Group.query.filter_by(name=name).first()

    def get_groups(self):
        return self.Group.query.all()

    def add_group_by_model(self, group: Group) -> Group:
        return self.add_model(group)

    def update_group_by_model(self, group: Group) -> Group:
        return self.update_model(group)

    def delete_group_by_model(self, group: Group) -> Group:
        return self.delete_model(group)

    def get_role_by_name(self, name: str):
        return self.Role.query.filter_by(name=name.lower()).first()

    def get_roles(self):
        return self.Role.query.all()

    def add_user_role(self, **kwargs):
        role = self.Role()
        for key, value in kwargs.items():
            setattr(role, key, value.strip().lower())
        return self.add_model(role)

    def add_user_role_model(self, model: Role) -> Role:
        return self.add_model(model)



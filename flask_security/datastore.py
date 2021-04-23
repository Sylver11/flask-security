class Datastore:
    def __init__(self, db):
        self.db = db

    def put(self, model):
        self.db.session.add(model)

    def update(self, model):
        self.db.session.merge(model)

    def delete(self, model):
        self.db.session.delete(model)

    def commit(self):
        from flask import current_app
        from sqlalchemy.exc import IntegrityError
        from sqlalchemy.exc import SQLAlchemyError
        try:
            self.db.session.commit()
            return True
        except IntegrityError as err:
            self.db.session.rollback()
            current_app.logger.error(err)
            return 'Integrity Error: Either duplication or foreign key error'
        except SQLAlchemyError as err:
            self.db.session.rollback()
            current_app.logger.error(err)
            return 'Fatal database error: Server Admin was informed'

    def add_model(self, model):
        self.put(model)
        return self.commit()

    def update_model(self, model):
        self.update(model)
        return self.commit()

    def delete_model(self, model):
        self.delete(model)
        return self.commit()


class UserDatastore(Datastore):

    def __init__(self, db, user_model, group_model, role_model):
        Datastore.__init__(self, db)
        self.user_model = user_model
        self.group_model = group_model
        self.role_model = role_model

    def get_user_by_uuid(self, uuid):
        return self.user_model.query.filter_by(uuid=uuid).first()

    def get_user_by_email(self, email):
        return self.user_model.query.filter_by(email=email).first()

    def get_group_by_name(self, name):
        return self.group_model.query.filter_by(name=name).first()

    def add_user(self, user_model):
        feedback = self.add_model(user_model)
        if isinstance(feedback, str):
            return feedback
        return user_model

    def update_user(self, user_model):
        feedback = self.update_model(user_model)
        if isinstance(feedback, str):
            return feedback
        return user_model

    def delete_user(self, user_model):
        feedback = self.delete_model(user_model)
        if isinstance(feedback, str):
            return feedback
        return None

    def add_group(self, group_model):
        self.put(group_model)
        feedback = self.commit()
        if isinstance(feedback, str):
            return feedback
        return group_model

    def update_group(self, group_model):
        self.update(group_model)
        feedback = self.commit()
        if feedback is None:
            return group_model
        return feedback

    def delete_group(self, group_model):
        self.delete(group_model)
        return self.commit()

    def add_user_role(self, **kwargs):
        role = self.role_model
        for key, value in kwargs.items():
            setattr(role, key, value.strip().lower())
        return self.add_model(role)

    def add_user_role_model(self, role_model):
        return self.add_model(role_model)

#    def prepare_user_role_and_add(self, role_name, role_description):
#        role_name = role_name.strip().lower()
#        role_description = role_description.strip().lower()
#        model = self.role_model(name=role_name,description=role_description)
#        return self.add_model(model)

    def get_role_by_name(self, role_name):
        role_name = role_name.lower()
        return self.role_model.query.filter_by(name=role_name).first()

    def get_roles(self):
        return self.role_model.query.all()


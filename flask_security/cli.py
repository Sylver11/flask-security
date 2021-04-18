from werkzeug.local import LocalProxy
from flask.cli import AppGroup
from flask import current_app
import click

security_cli = AppGroup('security')

_security = LocalProxy(lambda: current_app.extensions["security"])
_datastore = LocalProxy(lambda: _security._datastore)

@security_cli.command('get', help='email')
@click.argument('email')
def get_user_cli(email=None):
    pass

@security_cli.command('add-group')
@click.option('--group_name', prompt='Group Name',required=True)
@click.option('--admin_user_email', prompt='Admin User Email',required=True)
def add_group_cli(group_name, admin_user_email):
    user_model = _datastore.user_model
    user = user_model.query.filter_by(email=admin_user_email).first()
    if not user:
        raise click.UsageError('User not found.')
    if user.group:
        raise click.UsageError('User already part of another group')
    if user.group_admin:
        raise click.UsageError('User already admin of another group')
    group_model = _datastore.group_model
    group = group_model(name=group_name)
    group = _datastore.add_group(group)
    if isinstance(group, group_model):
        if group.uuid:
            user.group_uuid = group.uuid
            user.group_admin = True
            if not _datastore.update_user(user):
                raise click.UsageError('Failed: Could not update user details')
            click.echo('Success: Group successfully created')
        else:
            raise click.UsageError('Failed: Unkown reason')
    else:
        raise click.UsageError('Failed: Group name already in use.')
    return None

@security_cli.command('add-user',)
@click.option('--firstname', prompt='Firstname',required=True)
@click.option('--secondname', prompt='Secondname',required=True)
@click.option('--email', prompt='Email',required=True)
@click.password_option(required=True)
@click.option('--group',
        prompt='Group name (optional)',
        default='None',
        help='Leave empty for default')
def add_user_cli(firstname, secondname, email, password, group):
    user_model = _datastore.user_model
    user = user_model(
            firstname=firstname,
            secondname=secondname,
            email=email)
    user.set_password(password)
    if group != 'None':
        group = _datastore.get_group_by_name(group)
        if not group:
            raise click.UsageError('The specified group does not exist')
        user.group = group
    user = _datastore.add_user(user)
    if isinstance(user, user_model):
        if user.uuid:
            feedback = 'Success: User created'
            if user.group:
                feedback += ' and added to ' + user.group.name + ' group.'
            click.echo(feedback)
            return None
        else:
            raise click.UsageError('Unkown reason')
    else:
        raise click.UsageError('User already exists')
    return None

@security_cli.command('update', help='fname, sname, email, pass and role')
@click.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('user_details', nargs=-1, type=click.UNPROCESSED)
def update_user_cli(user_details):
    pass

@security_cli.command('delete', help='email')
@click.argument('email')
def delete_user_cli(email):
    pass


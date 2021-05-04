from werkzeug.local import LocalProxy
from flask.cli import AppGroup, with_appcontext
from flask import current_app
import click

security_cli = AppGroup('security')

security = LocalProxy(lambda: current_app.extensions["security"])
datastore = LocalProxy(lambda: security.datastore)


@with_appcontext
def check_if_user_exists_cli(ctx, param, email):
    user = datastore.get_user_by_email(email)
    if not user:
        raise click.UsageError('The specified user does not exist')
    return user.email

@with_appcontext
def check_if_duplicate_user_cli(ctx, param, email):
    user = datastore.get_user_by_email(email)
    if user:
        raise click.UsageError('The specified email already exists')
    return email

@with_appcontext
def check_if_duplicate_role_cli(ctx, param, name):
    role = datastore.get_role_by_name(name)
    if role:
        raise click.UsageError('The specified role already exists')
    return name


@security_cli.command('add-user',)
@click.option('--firstname',
        prompt='Firstname',
        required=True)
@click.option('--secondname',
        prompt='Secondname',
        required=True)
@click.option('--email',
        prompt='Email',
        callback=check_if_duplicate_user_cli,
        required=True)
@click.password_option(required=True)
@click.option('--group-name',
        prompt='Group name (optional)',
        default='')
def add_user_cli(*args, **kwargs):
    user = datastore.User(
            firstname=kwargs['firstname'],
            secondname=kwargs['secondname'],
            email=kwargs['email'])
    user.set_password(kwargs['password'])
    if kwargs['group_name']:
        group = datastore.get_group_by_name(kwargs['group_name'])
        if not group:
            raise click.UsageError('The specified group does not exist')
        user.add_group(group)
    user = datastore.add_user_by_model(user)
    if user.query_status:
        click.echo(user.query_response)
    else:
        raise click.UsageError(user.query_response)


@security_cli.command('update-user')
@click.option('--email',
        prompt='User Email',
        callback=check_if_user_exists_cli,
        required=True)
def update_user_cli(email):
    click.echo('Method not yet implemented')


@security_cli.command('delete-user')
@click.option('--email',
        prompt='User Email',
        callback=check_if_user_exists_cli)
def delete_user_cli(*args, **kwargs):
    user = datastore.delete_user_by_email(kwargs['email'])
    if user.query_status:
        click.echo(user.query_response)
    else:
        raise click.UsageError(user.query_response)


@security_cli.command('update-user-password')
@click.option('--email',
        prompt='User Email',
        callback=check_if_user_exists_cli,
        required=True)
def update_user_password(*args, **kwargs):
    user = datastore.get_user_by_email(kwargs['email'])
    user = datastore.update_user_by_model(user)
    if user.query_status:
        click.echo(user.query_response)
    else:
        raise click.UsageError(user.query_response)


@security_cli.command('show-user-detail')
@click.option('--email', prompt='User email',required=True)
def get_user_info_cli(email):
    user = datastore.get_user_by_email(email)
    if not user:
        raise click.UsageError('The specified user does not exist')
    click.echo(vars(user))


@security_cli.command('add-group')
@click.option('--group-name', prompt='Group Name',required=True)
@click.option('--admin-email', prompt='Admin User Email',required=True)
def add_group_cli(group_name, admin_email):
    user = datastore.User.query.filter_by(email=admin_email).first()
    if not user:
        raise click.UsageError('User not found.')
    group = datastore.Group(name=group_name, admin_uuid=user.uuid)
    group = datastore.add_group_by_model(group)
    if group.query_status:
        user.add_groups(group)
        user = datastore.update_user_by_model(user)
        if user.query_status:
            click.echo(user.query_response)
        else:
            raise click.UsageError(user.query_response)
    else:
        raise click.UsageError(group.query_response)


@security_cli.command('add-role',)
@click.option(
        '--role-name',
        prompt='Role Name',
        callback=check_if_duplicate_role_cli,
        required=True)
@click.option(
        '--role-description',
        prompt='Role Description',
        required=True)
def add_role_cli(*args, **kwargs):
    role = datastore.add_user_role(name=kwargs['role_name'],
            description=kwargs['role_description'])
    if role.query_status:
        click.echo(role.query_response)
    else:
        raise click.UsageError(role.query_response)


@security_cli.command('show-available-roles',)
def get_all_roles_cli():
    click.echo([r.name for r in datastore.get_roles()])


@security_cli.command('link-role-user')
@click.option('--email',
        prompt='User Email',
        callback=check_if_user_exists_cli,
        required=True)
@click.option('--role-name',
        prompt='Name of user role',
        required=True)
def link_role_with_user_cli(*args, **kwargs):
    user = datastore.get_user_by_email(kwargs['email'])
    role = datastore.get_role_by_name(kwargs['role_name'])
    if not role:
        raise click.UsageError('The specified role does not exist')
    user.add_roles(role)
    user = datastore.update_user_by_model(user)
    if user.query_status:
        click.echo(user.query_response)
    else:
        raise click.UsageError(user.query_response)





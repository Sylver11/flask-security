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
def check_if_duplicate_role_cli(ctx, param, name):
    role = datastore.get_role_by_name(name)
    if role:
        raise click.UsageError('The specified role already exist')
    return name


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
    group = datastore.Group(name=group_name, group_admin=user)
    datastore.add_group_by_model(group)
    if isinstance(group, object):
        if group.uuid:
            user.group = group
            datastore.update_user_by_model(user)
            if isinstance(user, object):
                click.echo('Success: Group successfully created')
            if instance(user, str):
                raise click.UsageError(user)
    elif isinstance(group, str):
        raise click.UsageError(group)
    else:
        raise click.UsageError('Could not add group for unknown reason')


@security_cli.command('add-user',)
@click.option('--firstname', prompt='Firstname',required=True)
@click.option('--secondname', prompt='Secondname',required=True)
@click.option('--email', prompt='Email',required=True)
@click.password_option(required=True)
@click.option('--group-name',
        prompt='Group name (optional)',
        default='')
def add_user_cli(firstname, secondname, email, password, group_name):
    User = datastore.User
    user = User(
            firstname=firstname,
            secondname=secondname,
            email=email)
    user.set_password(password)
    if group_name:
        group = datastore.get_group_by_name(group_name)
        if not group:
            raise click.UsageError('The specified group does not exist')
        user.add_group(group)
    response = datastore.add_user_by_model(user)
    if isinstance(response, str):
        raise click.UsageError(resonse)
    response = 'Successfully created user account for ' + user.firstname
    if group_name:
        response += ' and added to ' + group_name + ' group.'
    click.echo(response)


@security_cli.command('add-user-role',)
@click.option(
        '--role-name',
        prompt='Role Name',
        callback=check_if_duplicate_role_cli,
        required=True)
@click.option(
        '--role-description',
        prompt='Role Description',
        required=True)
def add_user_role_cli(name, description):
    role = datastore.add_user_role(name=name,description=description)
    if isinstance(role, str):
        raise click.UsageError(role)
    click.echo('Successfully created user role: ' + role.name)


@security_cli.command('show-available-roles',)
def get_all_roles_cli():
    click.echo([r.name for r in datastore.get_roles()])


@security_cli.command('link-role-user')
@click.option('--email',
        prompt='User Email',
        callback=check_if_user_exists_cli,
        required=True)
@click.option(
        '--role-name',
        prompt='Name of user role',
        required=True)
@click.pass_context
def link_role_with_user(*args, **kwargs):
    user = datastore.get_user_by_email(kwargs['email'])
    role = datastore.get_role_by_name(kwargs['role_name'])
    if not role:
        raise click.UsageError('The specified role does not exist')
    user.add_roles(role)
    user = datastore.update_user_by_model(user)
    if isinstance(user, str):
        raise click.UsageError(user)
    click.echo('Successfully linked ' + user.firstname + ' with ' + role.name )
    return None


@security_cli.command('update-user')
@click.option('--email',
        prompt='User Email',
        callback=check_if_user_exists_cli,
        required=True)
def update_user_cli(email):
    pass


@security_cli.command('delete-user')
@click.option('--email',
        prompt='User Email',
        callback=check_if_user_exists_cli,
        required=True)
def delete_user_cli(email):
    user = datastore.delete_user_by_email(email)
    if user is None:
        click.echo('Successfully deleted user with email:' + email )
    if isinstance(user, str):
        raise click.UsageError(user)
    else:
        raise click.UsageError('Failed to delete user for unknown reason')



from click.testing import CliRunner
from flask_security.cli import add_user_cli, update_user_cli,\
        delete_user_cli,\
        get_user_info_cli, add_group_cli, add_role_cli,\
        get_all_roles_cli, link_role_with_user_cli


def test_cli_manage_user(script_info):
    runner = CliRunner()

    # Missing params
    result = runner.invoke(
        add_user_cli, input='1234\n1234\n', obj=script_info)
    assert result.exit_code != 0

    # Create user
    result = runner.invoke(
        add_user_cli,
        ['--firstname','Justus',
            '--secondname', 'Voigt',
            '--email', 'connectmaeuse@gmail.com',
            '--password', '123456'],
        obj=script_info
    )
    assert result.exit_code == 0

    # Create same user again. Check for duplicate error
    result = runner.invoke(
        add_user_cli,
        ['--firstname','Justus',
            '--secondname', 'Voigt',
            '--email', 'connectmaeuse@gmail.com',
            '--password', '123456'],
        obj=script_info
    )
    assert result.exit_code == 2

    # Delete same user again
    result = runner.invoke(
        delete_user_cli,
        ['--email', 'connectmaeuse@gmail.com'],
        obj=script_info
    )
    assert result.exit_code == 0


def test_cli_manage_role(script_info):
    """Test create user CLI."""
    runner = CliRunner()

    # Missing params
    result = runner.invoke(
        add_role_cli,
        ['--role-name', 'superuser'],
        obj=script_info)
    assert result.exit_code != 0

    # Create role
    result = runner.invoke(
        add_role_cli,
        ['--role-name', 'superuser',
            '--role-description', 'Test description'],
        obj=script_info)
    assert result.exit_code == 0


def test_cli_manage_user_role_link(script_info):
    """Test add/remove role."""
    runner = CliRunner()

    # Create a user
    result = runner.invoke(
        add_user_cli,
        ['--firstname','Justus',
            '--secondname', 'Voigt',
            '--email', 'connectmaeuse@gmail.com',
            '--password', '123456'],
        obj=script_info
    )
    assert result.exit_code == 0

    # Create role
    result = runner.invoke(
        add_role_cli,
        ['--role-name', 'superuser',
            '--role-description', 'Test description'],
        obj=script_info)
    assert result.exit_code == 0

    # User not found
    result = runner.invoke(
        link_role_with_user_cli,
        ['--email','wrong_email@gmail.com',
            '--role-name', 'superuser'],
        obj=script_info)
    assert result.exit_code != 0

    # Link user with role
    result = runner.invoke(
        link_role_with_user_cli,
        ['--email','connectmaeuse@gmail.com',
            '--role-name', 'superuser'],
        obj=script_info)
    assert result.exit_code == 0


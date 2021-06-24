import djclick as click

from modelservice.simpl.syn import games_client


def echo(text, value):
    click.echo(
        click.style(text, fg='green') + '{0}'.format(value)
    )

def delete_run(run):
    """ Delete Run """
    echo('Resetting the Simpl Calc game run...', ' done')
    run.delete()


@click.command()
@click.option('--reset', default=False, is_flag=True,
              help="Delete game run and recreate it from scratch")
@click.option('--name', '-n', default='default', type=str,
              help='Name of run to create. (defaults to "default")')
def command(reset, name):
    """
    Create and initialize Simpl Calc game.
    Create a "default" Simpl Calc run.
    Set the run phase to "Play".
    Add 1 leader ("leader") to the run
    Add 2 players ("s1", "s2") to the run.
    Add a scenario and period 1 for each player.
    """

    # Create a Game
    game = games_client.games.get_or_create(
        name='Simpl Calc',
        slug='simpl-calc'
    )
    echo('getting or creating game: ', game.name)

    if reset:  # Handle resetting the run
        lookup = {'game': game.id, 'name': name}
        try:
            run = games_client.runs.get(**lookup)
        except games_client.ResourceNotFound:
            run = None
        except games_client.TypeError:
            run = None

        if run is not None:
            if click.confirm(
                    'Are you sure you want to delete the "{0}" game run and '
                    'recreate from scratch?'.format(name)):
                delete_run(run)

    # Create game Phases ("Play")
    play_phase = games_client.phases.get_or_create(
        game=game.id,
        name='Play',
        order=1,
    )
    echo('getting or creating phase: ', play_phase.name)

    # Add run with 2 players ready to play
    run = add_run(game, name, 2, play_phase, games_client)

    echo('Completed setting up run: id=', run.id)


def add_run(game, run_name, user_count, phase, games_client):
    # Create or get the Run
    run = games_client.runs.get_or_create(
        game=game.id,
        name=run_name,
    )
    echo('getting or creating run: ', run.name)

    # Set run to phase
    run.phase = phase.id
    run.save()
    echo('setting run to phase: ', phase.name)

    leader_user = games_client.users.get_or_create(
        password='leader',
        first_name='CALC',
        last_name='Leader',
        email='leader@calc.edu',
    )
    echo('getting or creating user: ', leader_user.email)

    games_client.runusers.get_or_create(
        user=leader_user.id,
        run=run.id,
        leader=True,
    )
    echo('getting or creating leader runuser for user: ', leader_user.email)

    user_name_root = "s"
    if run_name is not 'default':
        user_name_root = run_name

    for n in range(0, user_count):
        user_number = n + 1
        # Add player to run
        add_player(user_name_root, user_number, run, games_client)

    return run


def add_player(user_name_root, user_number, run, games_client):
    """Add player with name based on user_number to run with role"""

    username = '{}{}'.format(user_name_root, user_number)
    first_name = 'Student{0}'.format(user_number)
    email = '{0}@calc.edu'.format(username)

    user = games_client.users.get_or_create(
        password=username,
        first_name=first_name,
        last_name='User',
        email=email,
    )
    echo('getting or creating user: ', user.email)

    runuser = games_client.runusers.get_or_create(
        user=user.id,
        run=run.id,
        defaults={"role": None}
    )
    echo('getting or creating runuser for user: ', user.email)

    add_runuser_scenario(runuser, games_client)


def add_runuser_scenario(runuser, games_client):
    """Add a scenario named 'Scenario 1' to the runuser"""

    scenario = games_client.scenarios.get_or_create(
        runuser=runuser.id,
        name='Scenario 1',
    )
    click.echo('getting or creating runuser {} scenario: {}'.format(
        runuser.id,
        scenario.id))

    period = games_client.periods.get_or_create(
        scenario=scenario.id,
        order=1,
    )
    click.echo('getting or creating runuser {} period 1 for scenario: {}'.format(
        runuser.id,
        scenario.id))

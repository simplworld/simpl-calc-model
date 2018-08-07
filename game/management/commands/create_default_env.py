import djclick as click

from modelservice.simpl import games_client
from modelservice.utils.asyncio import coro


def echo(text, value):
    click.echo(
        click.style(text, fg='green') + '{0}'.format(value)
    )


async def delete_default_run(api_session):
    """ Delete default Run """
    echo('Resetting the Simpl Calc game default run...', ' done')
    game = await api_session.games.get_or_create(slug='simpl-calc')
    runs = await api_session.runs.filter(game=game.id)
    for run in runs:
        if run.name == 'default':
            await api_session.runs.delete(run.id)


@click.command()
@click.option('--reset', default=False, is_flag=True,
              help="Delete default game run and recreate it from scratch")
@coro
async def command(reset):
    """
    Create and initialize Simpl Calc game.
    Create a "default" Simpl Calc run.
    Set the run phase to "Play".
    Add 1 leader ("leader") to the run
    Add 2 players ("s1", "s2") to the run.
    Add a scenario and period 1 for each player.
    """

    async with games_client as api_session:

        # Handle resetting the game
        if reset:
            if click.confirm(
                    'Are you sure you want to delete the default game run and recreate from scratch?'):
                await delete_default_run(api_session)

        # Create a Game
        game = await api_session.games.get_or_create(
            name='Simpl Calc',
            slug='simpl-calc'
        )
        echo('getting or creating game: ', game.name)

        # Create game Phases ("Play")
        play_phase = await api_session.phases.get_or_create(
            game=game.id,
            name='Play',
            order=1,
        )
        echo('getting or creating phase: ', play_phase.name)

        # Add run with 2 players ready to play
        run = await add_run(game, 'default', 2, play_phase, api_session)

        echo('Completed setting up run: id=', run.id)


async def add_run(game, run_name, user_count, phase, api_session):
    # Create or get the Run
    run = await api_session.runs.get_or_create(
        game=game.id,
        name=run_name,
    )
    echo('getting or creating run: ', run.name)

    # Set run to phase
    run.phase = phase.id
    await run.save()
    echo('setting run to phase: ', phase.name)

    fac_user = await api_session.users.get_or_create(
        password='leader',
        first_name='CALC',
        last_name='Leader',
        email='leader@calc.edu',
    )
    echo('getting or creating user: ', fac_user.email)

    fac_runuser = await api_session.runusers.get_or_create(
        user=fac_user.id,
        run=run.id,
        leader=True,
    )
    echo('getting or creating leader runuser for user: ', fac_user.email)

    for n in range(0, user_count):
        user_number = n + 1
        # Add player to run
        await add_player(user_number, run, api_session)

    return run


async def add_player(user_number, run, api_session):
    """Add player with name based on user_number to run with role"""

    username = 's{0}'.format(user_number)
    first_name = 'Student{0}'.format(user_number)
    email = '{0}@calc.edu'.format(username)

    user = await api_session.users.get_or_create(
        password=username,
        first_name=first_name,
        last_name='User',
        email=email,
    )
    echo('getting or creating user: ', user.email)

    runuser = await api_session.runusers.get_or_create(
        user=user.id,
        run=run.id,
        defaults={"role": None}
    )
    echo('getting or creating runuser for user: ', user.email)

    await add_runuser_scenario(runuser, api_session)


async def add_runuser_scenario(runuser, api_session):
    """Add a scenario named 'Scenario 1' to the runuser"""

    scenario = await api_session.scenarios.get_or_create(
        runuser=runuser.id,
        name='Scenario 1',
    )
    click.echo('getting or creating runuser {} scenario: {}'.format(
        runuser.id,
        scenario.id))

    period = await api_session.periods.get_or_create(
        scenario=scenario.id,
        order=1,
    )
    click.echo('getting or creating runuser {} period 1 for scenario: {}'.format(
        runuser.id,
        scenario.id))

import asyncio

from django.conf import settings

from modelservice.profiler import ProfileCase
from modelservice.simpl import games_client_factory


class ProfileHttpTestCase(ProfileCase):
    """
    Profile HTTP calls from the modelservice to simpl-games-api.
    """

    async def profile_submit_decision(self):
        email = self.user_email
        if email is not None:
            print('profile_submit_decision: email=', email)

            # email format is <char><int>@ where <int> is 1..78
            # which assumes run name is a single letter
            decision = int(email[1:email.find('@')])

            # introduce a delay to prevent publish requests getting lost
            # await asyncio.sleep(decision)

            coro_client = games_client_factory()

            async with coro_client as coro_session:
                try:
                    # Determine Run and Runuser based on player email
                    run_name = email[0]  # run name is a single letter
                    run = await coro_session.runs.get(
                        game_slug=settings.GAME_SLUG,
                        name=run_name,
                    )
                    user = await coro_session.users.get(email=email)
                    runuser = await coro_session.runusers.get(
                        run=run.id,
                        user=user.id
                    )

                    # From here down, pull data from modelservice via WAMP

                    # First, emulate calls made by the simpl-react simpl decorator when a player logs in

                    runuser_topic = 'world.simpl.sims.simpl-calc.model.runuser.' + str(runuser.id)
                    # print('runuser_topic: ', runuser_topic)

                    #  getRunUsers(runuser_topic, false)
                    runusers_topic = runuser_topic + '.get_active_runusers'
                    await self.call(runusers_topic)  # ignore results

                    # getCurrentRunPhase(runuser_topic)
                    await self.call(runuser_topic + '.get_current_run_and_phase')  # ignore results

                    # getDataTree(runuser_topic)
                    get_scope_tree_uri = runuser_topic + '.get_scope_tree'
                    get_scope_tree_result = await self.call(get_scope_tree_uri)
                    # print(get_scope_tree_uri, '->')
                    # print(get_scope_tree_result)

                    # getRunUserScenarios(runuser_topic)
                    get_scenarios_uri = runuser_topic + '.get_scenarios'
                    get_scenarios_result = await self.call(get_scenarios_uri)
                    # print(get_scenarios_uri, '->')
                    # print(get_scenarios_result)

                    # getPhases('model:model.game')
                    get_phases_uri = 'world.simpl.sims.simpl-calc.model.game.get_phases'
                    get_phases_ = await self.call(get_phases_uri)
                    # print(get_phases_uri, '->')
                    # print(get_phases_)

                    # getRoles('model:model.game')
                    get_roles_uri = 'world.simpl.sims.simpl-calc.model.game.get_roles'
                    get_roles_result = await self.call(get_roles_uri)
                    # print(get_roles_uri, '->')
                    # print(get_roles_result)

                    # Next, prepare to submit player's decision

                    # get id of last period of player's scenario
                    periods = get_scope_tree_result['children'][0]['children']
                    # print('periods: ')
                    # print(periods)
                    last_period_id = periods[len(periods) - 1]['pk']
                    # print('last_period_id: ', last_period_id)

                except Exception as e:
                    print(e)
                    return

                # submit player's decision against the last period
                uri = 'world.simpl.sims.simpl-calc.model.period.' + str(last_period_id) + '.submit_decision'

                status = await self.call_as(email, uri, decision)
                if status != 'ok':
                    raise ValueError(
                        "submit_decision: status=" + status)


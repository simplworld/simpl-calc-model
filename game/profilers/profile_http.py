import asyncio

from django.conf import settings

from modelservice.profiler import ProfileCase
from modelservice.simpl import games_client_factory

PLAYER_DECISIONS = {
    "Price_Decision_P1": 0.54,
    "Price_Decision_P2": 0.66,
    "Breadth_Decision_P1": 0.50,
    "Breadth_Decision_P2": 0.50,
    "Depth_Decision_P1": 0.50,
    "Depth_Decision_P2": 0.50,
    "Private_Brand_Decision_P1": 0.50,
    "Private_Brand_Decision_P2": 0.50,
    "Online_Invest_Decision": 20000000,
    "Retail_Coverage_Decision": 200,
    "Customer_Service_Decision": 20000000,
    "Shopping_Experience_Decision": 20000000,
    "Vendor_Management_Decision": 60000000,
    "Customer_Analytics_Decision": 10000000,
    "Private_Brand_Quality_Decision": 5,
    "National_Brand_Quality_Decision": 5,
}


class ProfileHttpTestCase(ProfileCase):
    """
    Profile HTTP calls from the modelservice to simpl-games-api.
    """

    async def profile_submit_decisions(self):
        email = self.user_email
        if email is not None:
            # print('profile_submit_decisions: email=', email)
            #
            # email format is <char><int>@ where <int> is 1..78
            player_number = int(email[1:email.find('@')])
            # await asyncio.sleep(delay * 0.5)

            coro_client = games_client_factory()

            async with coro_client as coro_session:
                try:
                    # Determine Runuser based on player email
                    run_name = email[0]  # a, b, c, or d
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

                    world_topic = 'edu.upenn.sims.pop.model.world.' + str(
                        runuser.world)

                    #  getRunUsers(world_topic)
                    get_active_runusers_uri = world_topic + '.get_active_runusers'
                    get_active_runusers_result = await self.call(
                        get_active_runusers_uri)
                    # print(get_active_runusers_uri, '->')
                    # print(get_active_runusers_result)

                    # getCurrentRunPhase(world_topic)
                    get_current_run_and_phase_uri = world_topic + '.get_current_run_and_phase'
                    get_current_run_and_phase_result = await self.call(
                        get_current_run_and_phase_uri)
                    # print(get_current_run_and_phase_uri, '->')
                    # print(get_current_run_and_phase_result)

                    # getDataTree(world_topic)
                    get_scope_tree_uri = world_topic + '.get_scope_tree'
                    get_scope_tree_result = await self.call(get_scope_tree_uri)
                    # print(get_scope_tree_uri, '->')
                    # print(get_scope_tree_result)

                    runuser_topic = 'edu.upenn.sims.pop.model.runuser.' + str(
                        runuser.id)

                    #  getRunUsers(world_topic)
                    await self.call(
                        runuser_topic + '.get_active_runusers')  # ignore results

                    # getCurrentRunPhase(world_topic)
                    await self.call(
                        runuser_topic + '.get_current_run_and_phase')  # ignore results

                    # getDataTree(world_topic)
                    await self.call(
                        runuser_topic + '.get_scope_tree')  # ignore results

                    # getPhases('model:model.game')
                    get_phases_uri = 'edu.upenn.sims.pop.model.game.get_phases'
                    get_phases_ = await self.call(get_phases_uri)
                    # print(get_phases_uri, '->')
                    # print(get_phases_)

                    # getRoles('model:model.game')
                    get_roles_uri = 'edu.upenn.sims.pop.model.game.get_roles'
                    get_roles_result = await self.call(get_roles_uri)
                    # print(get_roles_uri, '->')
                    # print(get_roles_result)

                    # debug roe-ops#37
                    run_phase_name = \
                        get_current_run_and_phase_result['phase']['data'][
                            'name']
                    if run_phase_name != 'Play':
                        raise Exception("ERROR: Run must be in Play phase")

                    # get id of player's world scenario
                    scenario_id = get_scope_tree_result['children'][0]['pk']
                    # print('scenario_id: ', scenario_id)

                except Exception as e:
                    print(e)
                    return

                # assume each configured player is in a different team
                # print('player submitting decisions has email=', email)

                # submit world decisions
                submit_uri = \
                    'edu.upenn.sims.pop.model.scenario.' + \
                    str(scenario_id) + '.submit_world_decisions'

                status = await self.call_as(email,
                                            submit_uri,
                                            PLAYER_DECISIONS)
                if status != 'ok':
                    raise ValueError(
                        "submit_world_decisions: status=" + status)

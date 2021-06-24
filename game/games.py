from modelservice.games import Period, Game
from modelservice.games import subscribe, register

from .runmodel import step_scenario, save_decision


def log_wamp_details(log, details):
    # details is either autobahn.wamp.types CallerDetails or EventDetails
    if details is not None:
        log.info("details: {details!s}", details=details)


class SimplCalcPeriod(Period):
    @register
    async def submit_decision(self, operand, **kwargs):
        """
        Receives the operand played and stores as a ``Decision`` then
        steps the model saving the ``Result``. A new ``Period`` is added to
        scenario in preparation for the next decision.
        """
        # Call will prefix the ROOT_TOPIC
        # "world.simpl.sims.simpl-calc.model.period.1.submit_decision"

        for k in kwargs:
            self.session.log.info("submit_decision: Key: {}".format(k))

        self.session.log.info("submit_decision: operand: {}".format(operand))

        await save_decision(self.pk, operand)
        self.session.log.info("submit_decision: saved decision")

        await step_scenario(self.scenario.pk)
        self.session.log.info("submit_decision: stepped scenario")

        return 'ok'


class SimplCalcGame(Game):

    @register
    async def create_run(self, run_name, **kwargs):
        # Call will prefix the ROOT_TOPIC
        # "edu.upenn.sims.simpl-calc.model.game.create_run"

        self.session.log.info("SimplCalcGame: create_run: PK={pk}", pk=self.pk)
        log_wamp_details(self.session.log, kwargs['details'])

        result = {'celery_task_id': 0}
        result['error'] = 'Not implemented'

        return result


Game.register('simpl-calc', [
    SimplCalcGame, SimplCalcPeriod,
])

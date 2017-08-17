import daiquiri
from conference_scheduler import scheduler
from conference_scheduler.heuristics import hill_climber
from conference_scheduler.heuristics import simulated_annealing
from pulp import GLPK
from pulp import PULP_CBC_CMD

logger = daiquiri.getLogger(__name__)

solvers = {
    'pulp_cbc_cmd': {
        'function': scheduler.solution,
        'kwargs': {
            'objective_function': None,
            'solver': PULP_CBC_CMD(msg=False)}},
    'glpk': {
        'function': scheduler.solution,
        'kwargs': {
            'solver': GLPK(msg=False)}},
    'hill_climber': {
        'function': scheduler.heuristic,
        'kwargs': {
            'objective_function': None,
            'algorithm': hill_climber}},
    'simulated_annealing': {
        'function': scheduler.heuristic,
        'kwargs': {
            'objective_function': None,
            'algorithm': simulated_annealing}}}


def solution(events, slots, solver):
    logger.info(f'Scheduling conference using {solver} solver....')

    common_kwargs = {
        'events': events,
        'slots': slots,
    }

    kwargs = {**common_kwargs, **solvers[solver]['kwargs']}

    try:
        solution = solvers[solver]['function'](**kwargs)
    except ValueError:
        logger.error('No valid solution found')
        solution = None

    return solution

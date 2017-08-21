from datetime import datetime

import pytest
from conference_scheduler.resources import Event
from conference_scheduler.resources import Slot

import scheduler.denormalise as dn


@pytest.fixture
def event_types():
    return ['talk', 'workshop', 'plenary']


@pytest.fixture
def venues():
    return {
        'Assembly Room': {
            datetime(2017, 10, 26, 0, 0): {
                'morning': [
                    {
                        'starts_at': 36900,
                        'duration': 30,
                        'event_type': 'plenary',
                        'capacity': 600
                    },
                    {
                        'starts_at': 39600,
                        'duration': 30,
                        'event_type': 'plenary',
                        'capacity': 600
                    },
                ],
                'afternoon': [
                    {
                        'starts_at': 52200,
                        'duration': 30,
                        'event_type': 'talk',
                        'capacity': 600
                    },
                    {
                        'starts_at': 54000,
                        'duration': 30,
                        'event_type': 'talk',
                        'capacity': 600
                    }
                ]
            }
        }
    }


@pytest.fixture
def events_definition():
    return [
        {
            'title': 'UKPA AGM',
            'duration': 45,
            'tags': ['plenary'],
            'person': 'owen-campbell',
            'event_type': 'talk',
            'demand': 0
        },
        {
            'title': 'A very exciting talk',
            'duration': 30,
            'tags': ['talk'],
            'person': 'owen-campbell',
            'event_type': 'talk',
            'demand': 0
        },
        {
            'title': 'A very interesting talk',
            'duration': 30,
            'tags': ['talk'],
            'person': 'vincent-knight',
            'event_type': 'talk',
            'demand': 0
        },
        {
            'title': 'A slightly dull talk',
            'duration': 30,
            'tags': [],
            'person': 'joe-bloggs',
            'event_type': 'talk',
            'demand': 0
        },
        {
            'title': 'A fascinating workshop',
            'duration': 90,
            'tags': ['talk'],
            'person': 'alice',
            'event_type': 'workshop',
            'demand': 0
        },
        {
            'title': 'A beginner workshop',
            'duration': 90,
            'tags': ['talk'],
            'person': 'bob',
            'event_type': 'workshop',
            'demand': 0
        }
    ]


@pytest.fixture
def unavailability_defintion():
    return {
        'owen-campbell': [{
            'unavailable_from': datetime(2017, 10, 26, 0, 0),
            'unavailable_until': datetime(2017, 10, 26, 23, 59)
        }]
    }


@pytest.fixture
def clashes_definition():
    return {
        'owen-campbell': ['vincent-knight', 'joe-bloggs'],
        'vincent-knight': ['owen-campbell']
    }


@pytest.fixture
def allocations_definition():
    return [
        {'Another talk': {
            'person': 'charlie',
            'tags': None,
            'venue': 'Assembly Room',
            'day': datetime(2017, 10, 26, 0, 0),
            'session': 'afternoon',
            'starts_at': 54000}},
        {'Another workshop': {
            'person': 'diane',
            'tags': None,
            'venue': 'Room C',
            'day': datetime(2017, 10, 26, 0, 0),
            'session': 'afternoon',
            'starts_at': 54000}}]


def test_types_and_slots(event_types, venues):
    types_and_slots = dn.types_and_slots(venues)
    assert all(isinstance(item['slot'], Slot) for item in types_and_slots)
    assert len(types_and_slots) == 4


def test_types_and_events(events_definition):
    types_and_events = dn.types_and_events(events_definition)
    assert all(isinstance(item['event'], Event)for item in types_and_events)
    assert len(types_and_events) == 6


def test_unavailability(
    event_types, events_definition, venues, unavailability_defintion
):
    types_and_slots = dn.types_and_slots(venues)
    slots = [item['slot'] for item in types_and_slots]
    unavailability = dn.unavailability(
        events_definition, slots, unavailability_defintion)
    print(unavailability)
    assert list(unavailability.keys()) == [0, 1]


def test_clashes(events_definition, clashes_definition):
    clashes = dn.clashes(events_definition, clashes_definition)
    assert clashes == ({0: [2, 3, 1], 1: [2, 3, 0], 2: [0, 1], 3: [], 4: [], 5: []}, 2)


def test_unsuitability(venues, events_definition):
    types_and_slots = dn.types_and_slots(venues)
    unsuitability = dn.unsuitability(types_and_slots, events_definition)
    assert list(unsuitability.keys()) == list(range(6))


def test_allocations(allocations_definition):
    allocations = dn.allocations(allocations_definition)
    assert len(allocations) == len(allocations_definition)
    assert all(isinstance(item['event'], Event) for item in allocations)
    assert all(isinstance(item['slot'], Slot) for item in allocations)


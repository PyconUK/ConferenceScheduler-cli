from datetime import datetime

import pytest
from conference_scheduler.resources import Event
from conference_scheduler.resources import Slot

import scheduler.denormalise as dn


@pytest.fixture
def event_types():
    return ['talk', 'workshop', 'plenary']


@pytest.fixture
def days(event_types):
    return [
        datetime(2017, 10, 26, 0, 0),
        datetime(2017, 10, 27, 0, 0),
        datetime(2017, 10, 28, 0, 0),
        datetime(2017, 10, 29, 0, 0),
    ]


@pytest.fixture
def venues(days):
    return {
        'Assembly Room': {
            'capacity': 500,
            'suitable_for': ['talk', 'plenary'],
            'available': days},
        'Room A': {
            'capacity': 80,
            'suitable_for': ['workshop'],
            'available': days},
        'Ferrier Hall': {
            'capacity': 200,
            'suitable_for': ['talk'],
            'available': days},
        'Room C': {
            'capacity': 80,
            'suitable_for': ['talk', 'workshop'],
            'available': days},
        'Room D': {
            'capacity': 100,
            'suitable_for': ['talk'],
            'available': [datetime(2017, 10, 26, 0, 0)]}
    }


@pytest.fixture
def session_times():
    return {
        'plenary': {'None': [{'starts_at': 34200, 'duration': 45}]},
        'talk': {
            'morning': [
                {'starts_at': 36900, 'duration': 30},
                {'starts_at': 39600, 'duration': 30}
            ],
            'afternoon': [
                {'starts_at': 52200, 'duration': 30},
                {'starts_at': 54000, 'duration': 30}
            ]
        },
        'workshop': {
            'None': [
                {'starts_at': 36900, 'duration': 120},
                {'starts_at': 52200, 'duration': 120}
            ],
        }
    }


@pytest.fixture
def slot_times(session_times):
    return {
        'plenary': [
            {'duration': 45, 'session_name': 'None', 'starts_at': 34200}
        ],
        'talk': [
            {'duration': 30, 'session_name': 'morning', 'starts_at': 36900},
            {'duration': 30, 'session_name': 'morning', 'starts_at': 39600},
            {'duration': 30, 'session_name': 'afternoon', 'starts_at': 52200},
            {'duration': 30, 'session_name': 'afternoon', 'starts_at': 54000}
        ],
        'workshop': [
            {'duration': 120, 'session_name': 'None', 'starts_at': 36900},
            {'duration': 120, 'session_name': 'None', 'starts_at': 52200}
        ]
    }


@pytest.fixture
def events_definition():
    return [
        {
            'title': 'UKPA AGM',
            'duration': 45,
            'tags': ['plenary'],
            'person': 'owen-campbell',
            'event_type': 'talk'
        },
        {
            'title': 'A very exciting talk',
            'duration': 30,
            'tags': ['talk'],
            'person': 'owen-campbell',
            'event_type': 'talk'
        },
        {
            'title': 'A very interesting talk',
            'duration': 30,
            'tags': ['talk'],
            'person': 'vincent-knight',
            'event_type': 'talk'
        },
        {
            'title': 'A slightly dull talk',
            'duration': 30,
            'tags': [],
            'person': 'joe-bloggs',
            'event_type': 'talk'
        },
        {
            'title': 'A fascinating workshop',
            'duration': 90,
            'tags': ['talk'],
            'person': 'alice',
            'event_type': 'workshop'},
        {
            'title': 'A beginner workshop',
            'duration': 90,
            'tags': ['talk'],
            'person': 'bob',
            'event_type': 'workshop'
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


def test_slot_times(event_types, session_times, slot_times):
    assert dn.slot_times(event_types, session_times) == slot_times


def test_slots(event_types, venues, days, slot_times):
    slots = dn.slots(event_types, venues, days, slot_times)
    assert all(isinstance(slot, Slot) for slot in slots)
    assert len(slots) == 72


def test_events(event_types, events_definition):
    events = dn.events(events_definition)
    assert all(isinstance(event, Event)for event in events)
    assert len(events) == 6


def test_unavailability(
    event_types, events_definition, venues, days, slot_times,
    unavailability_defintion
):
    slots = dn.slots(event_types, venues, days, slot_times)
    unavailability = dn.unavailability(
        events_definition, slots, unavailability_defintion)
    print(unavailability)
    assert list(unavailability.keys()) == [0, 1]


def test_clashes(events_definition, clashes_definition):
    clashes = dn.clashes(events_definition, clashes_definition)
    assert clashes == {0: [2, 3, 1], 1: [2, 3, 0], 2: [0, 1], 3: [], 4: [], 5: []}


def test_unsuitability(
    venues, event_types, days, slot_times, events_definition
):
    slots = dn.slots(event_types, venues, days, slot_times)
    unsuitability = dn.unsuitability(venues, slots, events_definition)
    assert list(unsuitability.keys()) == list(range(6))

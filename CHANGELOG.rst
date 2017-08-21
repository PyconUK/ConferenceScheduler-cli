Changelog
#########

v0.7.2 (2017-08-21)
-------------------
* Bug Fix: Consistency optimisation fixed

v0.7.1 (2017-08-21)
-------------------
* Minor: Updated log message for Unavailability

v0.7.0 (2017-08-21)
-------------------
* Bug Fix: Remove use of strings for Slot.starts_at

* New Feature: Unavailability and clashes can now be defined for events as well
  as people

* New feature: Capacity objective now split into efficiency or equity

v0.6.0 (2017-08-18)
-------------------
* New Feature: Pre-allocated events can be defined in allocations.yaml

* Breaking Change: venues.yml renamed to timetable.yml

v0.5.0 (2017-08-17)
-------------------
* Breaking Change: content previously in separate yaml files now in venues.yaml

* New Feature: objective function argument added to build command

v0.4.1 (2017-08-16)
-------------------
* Improved logging with counts of events and slots by event type

v0.4.0 (2017-08-14)
-------------------
* New Feature: Venue availability can be defined

* Minor Improvement: Order of columns in schedule.csv swapped to show index
  numbers at lhs of file

v0.3.1 (2017-08-10)
-------------------
* Bug Fix: Redundant export of schedule on rebuild removed

v0.3.0 (2017-08-10)
-------------------
* New feature: Rebuild command
  Rebuild the output files from a previously computed schedule

v0.2.0 (2017-08-10)
-------------------
* New Featue: Validate command
  Validate a previously computed schedule

v0.1.0 (2017-08-10)
-------------------
* Initial release

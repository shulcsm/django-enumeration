Changes
=======

0.2.0 (2020-01-30)
------------------

* Update to django-enumfields 2.0.0

0.2.0 (2019-04-08)
------------------

* Update to django 2.2
* Update to django-enumfields 1.0.0
* Use native constraints for partial unique index.

SQL::

   ALTER INDEX enumeration_sequenc_5647e6_partial RENAME TO unique_counter_for_no_period;
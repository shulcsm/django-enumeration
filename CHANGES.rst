Changes
=======

2.0.0 (2024-12-09)
------------------
* move to uv
* Reassign number
* Return counter id

1.0.0 (2021-12-28)
------------------

* Remove to django-enumfields
* Use native django TextChoices
* Bump minimal django version to 3.2

0.2.2 (2021-12-28)
------------------

* Update to django-enumfields 2.1.1
* Test py38, py39 and django 3

0.2.1 (2020-01-30)
------------------

* Update to django-enumfields 2.0.0

0.2.0 (2019-04-08)
------------------

* Update to django 2.2
* Update to django-enumfields 1.0.0
* Use native constraints for partial unique index.

SQL::

   ALTER INDEX enumeration_sequenc_5647e6_partial RENAME TO unique_counter_for_no_period;

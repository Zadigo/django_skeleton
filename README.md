# Django Skeleton
A simple project that illustrates in a very simple manner how Django is initally setup starting from the `setup()` function.

The main registry populates itself with all registered apps and then uses the models of each of app as the pivotal point to update other instances in this order `Options`, `Field` and then `Manager` plus `MangerDescriptor`. 

To run the sequence call or debug the `_init.py` file.

Farthing: automatically add type annotations to Python source code by running it
================================================================================

Farthing will run arbitrary Python code while tracing the argument and return
types of all functions within a given file or directory. Farthing can then
automatically add type annotations based on the types of the values it saw
during the execution run.

For instance, the following code:

.. code-block:: python

    def factorial(n):
        result = 1
        
        for i in range(2, n + 1):
            result *= i
        
        return result

can be automatically transformed into:

.. code-block:: python

    def factorial(n: int) -> int:
        result = 1
        
        for i in range(2, n + 1):
            result *= i
        
        return result

by running Farthing against the following test file:

.. code-block:: python

    from nose.tools import assert_equal

    import fact


    def test_fib():
        test_cases = [
            (0, 1),
            (1, 1),
            (2, 2),
            (3, 6),
            (4, 24),
            (5, 120),
        ]
        
        for index, value in test_cases:
            yield _check_fact, index, value


    def _check_fact(index, value):
        assert_equal(value, fact.factorial(index))
        
Usage
~~~~~

Farthing can be called from the command line. The first argument should be the
file or directory that should have type annotations added to it. The other
arguments should be the Python script to run with any arguments. For instance:

.. code-block:: sh

    farthing demo/fact.py _virtualenv/bin/nosetests demo/tests.py


Demo
~~~~

To run the demo, you can just run ``demo.sh``. To explain what it actually does:

#. Run ``make bootstrap`` to set up the virtualenv with dependencies.

#. Run ``. _virtualenv/bin/activate`` to enter the virtualenv.

#. Run ``farthing demo/fact.py _virtualenv/bin/nosetests demo/tests.py`` to
   run ``_virtualenv/bin/nosetests demo/tests.py`` and add annotations to
   ``demo/fact.py`` based on the types of actual values used in the execution run.

Limitations
~~~~~~~~~~~

At the moment, Farthing is just a quick prototype, so currently has the
following limitations:

* Annotations are added just using the name of the type, which may not be
  available in the current scope.

* Type annotations cannot be added to the Python script being run.

* The first type seen is used, rather than any attempt at finding a super-type.

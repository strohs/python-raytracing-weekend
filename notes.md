activating a virtual environment
> source venv/bin/activate


## unit testing
to test a specific module
> python -m unittest -v tests/test_something.py

to use "test discovery"
> python -m unittest

OR
> python -m unittest discover

OR specify a specific directory (named "tests" in this case) with verbose output
> python -m unittest discover -v tests


`-t` option can be used to specify the top level directory
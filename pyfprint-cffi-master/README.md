pyfprint-cffi
=============

tl;dr
-----
This is a python module with [CFFI](https://cffi.readthedocs.org/en/latest/) bindings for [libfprint](http://www.freedesktop.org/wiki/Software/fprint/libfprint/)

**warning:** i've cut off some things from the [original](https://github.com/xantares/pyfprint) [SWIG](https://github.com/swig/swig) bindings

usage
-----

	mkdir venv
	. venv/bin/activate
	pip install .
	# hack hack hack

story
-----

It's forked from [@luksan](https://github.com/luksan) [original work](https://github.com/luksan/pyfprint),
which was then improved by [@xantares](https://github.com/xantares) [here](https://github.com/xantares/pyfprint) with Python 3 support.

The original SWIG version had issues with surrogate strings on modern python versions ([an issue has been filed](https://github.com/swig/swig/issues/222)), and I failed in working around it *so bad*.

Reimplementing just the needed stuff using CFFI (*and possibly having broken everything else*) turned out to be a great idea :)

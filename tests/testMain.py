template = """

from distutils.core import setup, Extension

import sys
import pprint

from Cython.Distutils import build_ext

ext = Extension("test_files/out.cpp", language="c++",
        include_dirs = %(include_dirs)r,
        extra_compile_args = [],
        extra_link_args = [],
        )

setup(cmdclass = {'build_ext' : build_ext},
      name="test_main",
      version="0.0.1",
      ext_modules = [ext]
     )

"""

def test_run():
    from autowrap.Main import run
    from autowrap.Utils import compile_and_import

    import glob

    pxds = glob.glob("test_files/pxds/*.pxd")
    assert pxds

    addons = glob.glob("test_files/addons/*.pyx")
    assert addons

    converters = glob.glob("test_files/converters/*.py")
    assert converters

    extra_includes = ["test_files/includes"]
    includes = run(pxds, addons, converters, "test_files/out.pyx",
            extra_includes)

    mod = compile_and_import("out", ["test_files/out.cpp"], includes)

    ih = mod.IntHolder()
    ih.set_(3)
    assert ih.get() == 3

    # automatic IntHolder <-> it conversions:
    b = mod.B()
    b.set_(7)
    assert b.get() == 7

    # manually generated method
    assert b.super_get(3) == 4

    # uses extra cimport for M_PI
    assert abs(b.get_pi()-3.141) < 0.001

    # manual class:
    assert mod.C.c == 3
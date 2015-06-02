#!/usr/bin/env python3

"""Unit tests for the PySpiro _native module."""

# Copyright © 2015 Timothy Pederick.
# Based on libspiro:
#     Copyright © 2007 Raph Levien
#
# This file is part of PySpiro.
#
# PySpiro is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PySpiro is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PySpiro. If not, see <http://www.gnu.org/licenses/>.

# Standard library imports.
import ctypes
import unittest

# Module to be tested.
from spiro import _native

# Test cases.
class TestDataStructures(unittest.TestCase):
    """Test Python equivalents of libspiro data structures."""
    def test_bezctx_structure(self):
        """Check the definition of the bezctx structure."""
        self.assertTrue(issubclass(_native.bezctx, ctypes.Structure))
        self.assertEqual(len(_native.bezctx._fields_), 5)

        expected_names = {'moveto', 'lineto', 'quadto', 'curveto', 'mark_knot'}
        for fieldname, fieldtype in _native.bezctx._fields_:
            self.assertIn(fieldname, expected_names)
            expected_names.discard(fieldname)
            # Function wrappers generated by ctypes.CFUNCTYPE call themselves
            # 'CFunctionType', but that appears to be a private ctypes class,
            # so we settle for checking their repr() instead.
            self.assertEqual(repr(fieldtype), "<class 'ctypes.CFunctionType'>")
            self.assertTrue(callable(fieldtype))
        self.assertEqual(len(expected_names), 0)

    def test_CPType_enum(self):
        """Check the definition of the CPTypes enumeration."""
        self.assertEqual(len(_native.CPType), 8)

        self.assertEqual(_native.CPType.corner,           b'v')
        self.assertEqual(_native.CPType.g4,               b'o')
        self.assertEqual(_native.CPType.g2,               b'c')
        self.assertEqual(_native.CPType.left,             b'[')
        self.assertEqual(_native.CPType.right,            b']')
        self.assertEqual(_native.CPType.end,              b'z')
        self.assertEqual(_native.CPType.open_contour,     b'{')
        self.assertEqual(_native.CPType.end_open_contour, b'}')

    def test_spiro_cp_structure(self):
        """Check the definition of the spiro_cp structure."""
        self.assertTrue(issubclass(_native.spiro_cp, ctypes.Structure))
        self.assertEqual(len(_native.spiro_cp._fields_), 3)

        expected_fields = {'x': ctypes.c_double,
                           'y': ctypes.c_double,
                           'ty': ctypes.c_char}
        for fieldname, fieldtype in _native.spiro_cp._fields_:
            expected_type = expected_fields.get(fieldname)
            self.assertIsNotNone(expected_type)
            self.assertIs(fieldtype, expected_type)


class TestNativeFunctions(unittest.TestCase):
    """Test ctypes wrappers of native functions."""
    def is__FuncPtr(self, fn):
        """Test whether a function is an instance of ctypes._FuncPtr."""
        # Callable foreign functions are instances of the private ctypes class
        # '_FuncPtr', so we settle for checking its repr() instead.
        return repr(fn).startswith('<_FuncPtr object at ')
        
    def test_SpiroCPsToBezier_wrapper(self):
        """Test the wrapper of the SpiroCPsToBezier() function."""
        self.assertTrue(self.is__FuncPtr(_native.SpiroCPsToBezier))
        self.assertTrue(callable(_native.SpiroCPsToBezier))
        self.assertEqual(len(_native.SpiroCPsToBezier.argtypes), 4)
        self.assertIsNone(_native.SpiroCPsToBezier.restype)

    def test_TaggedSpiroCPsToBezier_wrapper(self):
        """Test the wrapper of the SpiroCPsToBezier() function."""
        self.assertTrue(self.is__FuncPtr(_native.TaggedSpiroCPsToBezier))
        self.assertTrue(callable(_native.TaggedSpiroCPsToBezier))
        self.assertEqual(len(_native.TaggedSpiroCPsToBezier.argtypes), 2)
        self.assertIsNone(_native.TaggedSpiroCPsToBezier.restype)
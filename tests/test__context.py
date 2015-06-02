#!/usr/bin/env python3

"""Unit tests for the PySpiro _context module."""

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
import io
import unittest

# Module to be tested.
from spiro import _context

# Test cases.
class TestBezierContext(unittest.TestCase):
    """Test the BezierContext abstract class."""
    def test_not_instantiable(self):
        """Ensure that BezierContext cannot be instantiated."""
        self.assertRaises(NotImplementedError, _context.BezierContext)

    def test_abstract_functions(self):
        """Check whether abstract functions are present and abstract."""
        # This also implicitly checks whether they accept the right number of
        # arguments; otherwise, a TypeError results instead of the expected
        # NotImplementedError.
        for fn_name, arg_count in (('moveto', 5),
                                   ('lineto', 4),
                                   ('quadto', 6),
                                   ('curveto', 8)):
            fn = getattr(_context.BezierContext, fn_name)
            self.assertRaises(NotImplementedError, fn, *([None] * arg_count))

    def test_mark_knot(self):
        """Test mark_knot(), the only concrete function."""
        self.assertIsNone(_context.BezierContext.mark_knot(None, None, None))

class TestSVGPathContext(unittest.TestCase):
    """Test the SVGPathContext class."""
    def setUp(self):
        """Create a StringIO buffer to hold output."""
        self.buffer = io.StringIO()

    def tearDown(self):
        """Close the StringIO buffer."""
        self.buffer.close()

    def test_moveto(self):
        """Test the moveto() method."""
        with _context.SVGPathContext(self.buffer) as ctx:
            ctx.moveto(None, 40, -20, False)
            ctx.moveto(None, 30, 0, True)
            ctx.moveto(None, 0, 10, False)
        self.assertEqual(self.buffer.getvalue(), 'M40,-20 Z M30,0 M0,10 Z')

    def test_lineto(self):
        """Test the lineto() method."""
        with _context.SVGPathContext(self.buffer) as ctx:
            ctx.lineto(None, 314, 159)
        self.assertEqual(self.buffer.getvalue(), 'L314,159 ')

    def test_quadto(self):
        """Test the quadto() method."""
        with _context.SVGPathContext(self.buffer) as ctx:
            ctx.quadto(None, 42, 13, 7, 3)
        self.assertEqual(self.buffer.getvalue(), 'Q42,13 7,3 ')

    def test_curveto(self):
        """Test the curveto() method."""
        with _context.SVGPathContext(self.buffer) as ctx:
            ctx.curveto(None, 1, 1, 2, 3, 5, 8)
        self.assertEqual(self.buffer.getvalue(), 'C1,1 2,3 5,8 ')

    def test_closing(self):
        """Check that a final close-path command is generated if needed."""
        with _context.SVGPathContext(self.buffer) as ctx:
            ctx.moveto(None, 1, 2, False)
        self.assertEqual(self.buffer.getvalue(), 'M1,2 Z')

    def test_no_closing(self):
        """Check that an exception prevents a final close-path command."""
        try:
            with _context.SVGPathContext(self.buffer) as ctx:
                ctx.moveto(None, 1, 2, False)
                ctx.moveto() # raises TypeError
        except TypeError:
            pass
        self.assertEqual(self.buffer.getvalue(), 'M1,2 ')

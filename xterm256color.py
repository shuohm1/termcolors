#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import sys

DEFAULTS = 16
DEF_BREAKS = 8

RGB_MAX = 2 ** 8 - 1
RGB_GRADS = 6
RGB_BASE = 55
RGB_STEP = (RGB_MAX - RGB_BASE) // (RGB_GRADS - 1)
RGB_BREAKS = RGB_GRADS

GRAY_MAX = 2 ** 8 - 18
GRAY_GRADS = 24
GRAY_BASE = 8
GRAY_STEP = (GRAY_MAX - GRAY_BASE) // (GRAY_GRADS - 1)
GRAY_BREAKS = DEF_BREAKS

DESCRIPTION = "Show default colors of 'xterm-256color'."
EPILOG = """
This script shows color codes in the form of 'xx#rrggbb'.
The 'xx' represents an indexed color code,
and the 'rrggbb' represents a RGB color code.
Note: if you changed color-pallet settings,
indexed color codes and RGB color codes are not correspond.
"""

def rgb_range(grads):
	for i in range(grads):
		x = i * RGB_STEP
		if i > 0:
			x += RGB_BASE
		yield (i, x)

def gray_range(grads):
	for i in range(grads):
		yield (i, i * GRAY_STEP + GRAY_BASE)

def main():
	s = "{e}[38;5;{{code:d}}m{{code:02x}}#{{hexs}}{e}[m"
	t = s.format(e="\033")

	h = "******"
	for c in range(DEFAULTS):
		print(t.format(code=c, hexs=h), end="")
		if (c + 1) % DEF_BREAKS > 0:
			print(" ", end="")
		else:
			print()
	base = c + 1

	for i, r in rgb_range(RGB_GRADS):
		for j, g in rgb_range(RGB_GRADS):
			for k, b in rgb_range(RGB_GRADS):
				c = base + i * RGB_GRADS ** 2 + j * RGB_GRADS + k
				h = "{r:02x}{g:02x}{b:02x}".format(r=r, g=g, b=b)
				print(t.format(code=c, hexs=h), end="")
				if (c - base + 1) % RGB_BREAKS > 0:
					print(" ", end="")
				else:
					print()
	base = c + 1

	for i, k in gray_range(GRAY_GRADS):
		c = base + i
		h = "{k:02x}{k:02x}{k:02x}".format(k=k)
		print(t.format(code=c, hexs=h), end="")
		if (c - base + 1) % GRAY_BREAKS > 0:
			print(" ", end="")
		else:
			print()
	base = c + 1

	return 0

def parse(argv):
	parser = argparse.ArgumentParser(description=DESCRIPTION,
	                                 epilog=EPILOG)
	return parser.parse_args(argv)

if __name__ == "__main__":
	sys.exit(main(**vars(parse(sys.argv[1:]))))

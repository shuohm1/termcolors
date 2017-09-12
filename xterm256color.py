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

def print_codelines(lines):
	for codes in lines:
		print(" ".join(codes))

def main(show_basic=False, show_colorful=False, show_gray=False):
	show_all = not (show_basic or show_colorful or show_gray)

	s = "{e}[38;5;{{code:d}}m{{code:02x}}#{{hexs}}{e}[m"
	t = s.format(e="\033")
	base = 0

	if show_basic or show_all:
		h = "******"
		basic_codes = []
		basic_codelines = []
		for c in range(DEFAULTS):
			basic_codes.append(t.format(code=c, hexs=h))
			if (c + 1) % DEF_BREAKS == 0:
				basic_codelines.append(basic_codes)
				basic_codes = []
		print_codelines(basic_codelines)
	base += DEFAULTS

	if show_colorful or show_all:
		colorful_codes = []
		colorful_codelines = []
		for i, r in rgb_range(RGB_GRADS):
			for j, g in rgb_range(RGB_GRADS):
				for k, b in rgb_range(RGB_GRADS):
					c = base + i * RGB_GRADS ** 2 + j * RGB_GRADS + k
					h = "{r:02x}{g:02x}{b:02x}".format(r=r, g=g, b=b)
					colorful_codes.append(t.format(code=c, hexs=h))
					if (c - base + 1) % RGB_BREAKS == 0:
						colorful_codelines.append(colorful_codes)
						colorful_codes = []
		print_codelines(colorful_codelines)
	base += RGB_GRADS ** 3

	if show_gray or show_all:
		gray_codes = []
		gray_codelines = []
		for i, k in gray_range(GRAY_GRADS):
			c = base + i
			h = "{k:02x}{k:02x}{k:02x}".format(k=k)
			gray_codes.append(t.format(code=c, hexs=h))
			if (c - base + 1) % GRAY_BREAKS == 0:
				gray_codelines.append(gray_codes)
				gray_codes = []
		print_codelines(gray_codelines)
	base += GRAY_GRADS

	return 0

def parse(argv):
	parser = argparse.ArgumentParser(description=DESCRIPTION,
	                                 epilog=EPILOG)
	parser.add_argument("-b", "--basic", dest="show_basic",
	                    action="store_true", default=False,
	                    help="show basic color codes")
	parser.add_argument("-c", "--colorful", dest="show_colorful",
	                    action="store_true", default=False,
	                    help="show RGB color codes")
	parser.add_argument("-g", "--gray", dest="show_gray",
	                    action="store_true", default=False,
	                    help="show gray color codes")
	return parser.parse_args(argv)

if __name__ == "__main__":
	sys.exit(main(**vars(parse(sys.argv[1:]))))

#!/usr/bin/env python

from __future__ import print_function
from collections import namedtuple
from datetime import datetime
import jinja2
import os
import re
import sys

MATCHER = re.compile(r'\.icon-([\w\d-]+):before { content: "\\f([\d\w]+)"; }')

Icon = namedtuple('Icon', ['name', 'code'])


def number_to_name(num):
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
            'eight', 'nine', 'ten', 'eleven'][num]


def sanitize_name(name):
    numbers_replaced = re.sub(r'(\d+)',
                              lambda m: number_to_name(int(m.group(1))),
                              name)
    return 'mf' + ''.join([s.capitalize()
                          for s in numbers_replaced.split('-')])


def sanitize_code(code):
    return re.sub('(\w)', lambda m: m.group(1).upper(), code)


def load_icons(filename):
    with open(filename) as f:
        return [Icon(sanitize_name(m[0]), sanitize_code(m[1]))
                for m in MATCHER.findall(f.read())]


def load_template(filename):
    env = jinja2.Environment(
      block_start_string='\BLOCK{',
      block_end_string='}',
      variable_start_string='\VAR{',
      variable_end_string='}',
      trim_blocks=True,
      autoescape=False,
      loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    return env.get_template(filename)


def package_version_date_format(date):
    return date.isoformat().replace('-', '/')


def render(template_name, icons):
    template = load_template(template_name)
    outfile = template_name.replace('_template', '')
    with open(outfile, 'w') as of:
        of.write(template.render(date=package_version_date_format(
                                   datetime.now().date()),
                                 icons=icons))


ICON_CSS_FILENAME = 'font-mfizz/dist/font-mfizz.css'

if __name__ == '__main__':
    icons = load_icons(ICON_CSS_FILENAME)
    for template in sys.argv[1:]:
        render(template, icons)

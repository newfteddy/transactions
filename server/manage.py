#!/usr/bin/env python
import os
import sys
#os.environ['ARTM_SHARED_LIBRARY'] = '../backend/bigartm_lib/lib/libartm.so'
sys.path.append('../backend/code')
#sys.path.append('../backend/bigartm/python')

from transform import init_chart

if __name__ == "__main__":
    init_chart()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serverapp.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


#!/usr/bin/env python2
import datetime as dt
import glob as glob
import os as os
import re
import shutil as shutil
import signal as signal
import subprocess as sp
import sys as sys

def help_message():
    print('Use the flags -i and -s for the input file and current stage of the calculations')
    print('Example: python BAT.py -i input.in -s equil')


def check_input(param_type, param_value, filename, param_name):
    if not param_value:
    # If the parameter value was not defined	
         if param_type == 'string':
             return 'None'
         elif param_type == 'list':
             return []
         elif param_type == 'float':
             return 0.0
         elif param_type == 'int':
             return 0
    # If the value is provided in the input file, check for correct format
    if param_type == 'float':
        try:
            float(param_value)
        except ValueError:
            print(param_value)
            print('Use a floating point value for %s in the input file' % param_name)
            sys.exit()

        return float(param_value)

    elif param_type == 'int':
        try:
            int(param_value)
        except ValueError:
            print(param_value)
            print('Use an integer value for %s in the input file' % param_name)
            sys.exit()

        if int(param_value) < 0:
            print(param_value)
            print('Use a non-negative value for %s in the input file' % param_name)
            sys.exit()
        else:
            return int(param_value)

    elif (param_type == 'list') or (param_type == 'string'):
        return param_value


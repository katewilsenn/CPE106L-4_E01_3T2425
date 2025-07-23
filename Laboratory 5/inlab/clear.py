"""
  File: clear.py
"""

import os
import platform

def clearSYS():
  if platform.system() == "Windows": os.system('cls')
  else: os.system('clear')

import csv
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def Cb_safe_div(x,y):
    if y == 0:
        return 1
    return x/y

def Cap(x,lower,upper):
    if x < lower:
        x = lower
    elif x > upper:
        x = upper
    return x

def None2Zero(value):
    if value == '':
        value = '0'
    return value

def contains(A,B):
    for i in A:
        if i in B: return True
    else: return False

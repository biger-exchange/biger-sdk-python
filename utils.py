#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import random
import string

def day_get(d):
  date_from = datetime.datetime(d.year, d.month, d.day, 0, 0, 0)
  return date_from.strftime("%s")

def week_get(d):
  dayscount = datetime.timedelta(days=(d.isoweekday() -1 -7))
  dayfrom = d - dayscount
  date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
  return date_from.strftime("%s")

def month_get(d):
  date_from = datetime.datetime(d.year, d.month, 1, 0, 0, 0)
  return date_from.strftime("%s")

def year_get(d):
  date_from = datetime.datetime(d.year, 1, 1, 0, 0, 0)
  return date_from.strftime("%s")

def getrds(N):
  return ''.join(random.SystemRandom().choice(string.digits + string.ascii_lowercase) for _ in range(N))

def getrdn(N):
  return int(''.join(random.SystemRandom().choice(string.digits) for _ in range(N)))
  
def getrdf(N):
  s="0." + '0'*(N-1) + "1"
  e="0." + '9'*N 
  return round(random.uniform(float(s),float(e)),N)  


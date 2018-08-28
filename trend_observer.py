from __future__ import division
import time

class TrendObserver(object):
  def __init__(self):
      self._start_value = None
      self._start_time = None
      self._trend = None
      self._interval = None

  def compute_trend(self, value):
      if self._start_value is None and self._start_time is None:
          self._start_value = value
          self._start_time = time.time()
      else:
          abs_start_value = abs(self._start_value)
          end_time = time.time()
          self._trend = (value - self._start_value) * 100 / abs_start_value
          self._interval = end_time - self._start_time
          self._start_value = value
          self._start_time = end_time
      #endelse

  def get_trend(self):
      return self._trend

  def get_interval(self):
      return self._interval
  #enddef

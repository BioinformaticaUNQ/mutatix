import sys

class MutatixPrinter():
  def __init__(self, info, debug, error):
    self._info = info
    self._debug = debug
    self._error = error

  def log(self, message):
    self._info(message)

  def debug(self, message):
    self._debug('debug message start *********************************************************************')
    self._debug(message)
    self._debug('debug message end   *********************************************************************')

  def error(self, fx):
    e = sys.exc_info()
    self._error('error message start *********************************************************************')
    self._error(fx(e))
    self._error('error message end   *********************************************************************')

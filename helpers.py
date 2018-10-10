"""Utilities for interpreting data that arrives in impractical formats.

This module stores helper functions that transform data for the controllers.
"""

class NotFoundError(Exception):
  def __init__(self, id):
    self.message = "Entity could not be found with id {}".format(id)

def get_traffic(connection, id):
  """Collects data about a single paper's download statistics.

  Arguments:
    - connection: a database connection object.
    - id: the ID given to the article being queried.
  Returns:
    - A two-element tuple. The first element is the number of views of
        the paper's abstract; the second is total PDF downloads.

  """

  traffic = connection.read("SELECT SUM(abstract), SUM(pdf) FROM article_traffic WHERE article={};".format(id))
  if len(traffic) == 0:
    raise NotFoundError(id)
  return traffic[0] # "traffic" is an array of tuples; we only want a tuple.

def num_to_month(monthnum):
  """Converts a (1-indexed) numerical representation of a month
  of the year into a three-character string for printing. If
  the number is not recognized, it returns an empty string.

  """
  months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
  }
  if monthnum is None or monthnum < 1 or monthnum > 12:
    return ""
  return months[monthnum]

def formatCategory(cat):
  return cat.replace("-", " ")

def formatNumber(val):
  if val is None:
    return "None"
  return format(val, ",d")
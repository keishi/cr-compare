#!/usr/bin/env python

import os
import re
import subprocess
import logging
import optparse
import platform
import multiprocessing
import time
import math
import tempfile
import json
import fnmatch
import sys
import csv

logging.basicConfig(level=logging.WARN, format='\033[1m%(asctime)s %(levelname)s : %(message)s\033[0m')

def IsWindows():
  """Returns true if the platform is Windows."""
  return os.uname()[0].startswith("CYGWIN_NT")


def IsMac():
  """Returns true if the platform is Mac."""
  return os.name == 'posix' and os.uname()[0] == 'Darwin'


def IsLinux():
  """Returns true if the platform is Linux."""
  return os.name == 'posix' and os.uname()[0] == 'Linux'


def IsChromiumSrcDir(dir_path):
  git_config_path = os.path.join(dir_path, ".git/config")
  if not os.path.exists(git_config_path) or not os.path.isfile(git_config_path):
    return False
  f = open(git_config_path, "r")
  result = False
  while True:
    line = f.readline()
    if not line:
      break
    elif line.find("/chromium/src.git") > -1:
      result = True
      break
  f.close()
  return result


def LocateChromiumDir(path):
  while True:
    if IsChromiumSrcDir(path):
      return path
    if path == "/":
      break
    path = os.path.dirname(path)
  path = os.path.join(os.getenv("CHROMIUM_DIR"), "src")
  if IsChromiumSrcDir(path):
    return path
  return None

def call_command(commands, env=os.environ):
  logging.info(commands);
  process = subprocess.Popen(commands, env=env)
  process.wait()
  return process.returncode

t_distribution = [None, None, 12.71, 4.30, 3.18, 2.78, 2.57, 2.45, 2.36, 2.31, 2.26, 2.23, 2.20, 2.18, 2.16, 2.14, 2.13, 2.12, 2.11, 2.10, 2.09, 2.09, 2.08, 2.07, 2.07, 2.06, 2.06, 2.06, 2.05, 2.05, 2.05, 2.04, 2.04, 2.04, 2.03, 2.03, 2.03, 2.03, 2.03, 2.02, 2.02, 2.02, 2.02, 2.02, 2.02, 2.02, 2.01, 2.01, 2.01, 2.01, 2.01, 2.01, 2.01, 2.01, 2.01, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.96]

def t_dist(n):
  if n >= len(t_distribution):
    return 1.96
  return t_distribution[n]

def compute_mean(series):
  if len(series) == 0:
    return 0
  sum = 0
  for value in series:
    sum += value
  return sum / len(series)

def compute_std_dev(series):
  if len(series) <= 1:
    return float('inf')
  mean = compute_mean(series)
  delta_squared_sum = 0;
  for value in series:
    delta_squared_sum += (value - mean) ** 2
  variance = delta_squared_sum / (len(series) - 1);
  return math.sqrt(variance);

def compute_std_err(series):
  std_dev = compute_std_dev(series)
  return std_dev / math.sqrt(len(series))

def lookup_bigger_is_better(units):
  if units in ['fps', 'runs/s', 'score']:
    return True
  if units in ['ms', '%', 'count', 'kb', 'percent', 'mWh']:
    return False
  logging.error('Unknown unit "%s". Please add entry to lookup_bigger_is_better function.' % units)
  exit()

def compute_summary(a, b, bigger_is_better):
    mean_a = compute_mean(a)
    mean_b = compute_mean(b)
    std_err_a = compute_std_err(a)
    std_err_b = compute_std_err(b)
    if std_err_a == 0 and std_err_b == 0:
      return 'N/A', False
    t = (mean_a - mean_b) / math.sqrt(std_err_a ** 2 + std_err_b ** 2);
    df = len(a) + len(b) - 2
    statistically_significant = abs(t) > t_dist(df + 1)
    diff = mean_b - mean_a;
    if mean_a == 0:
      diff_percentage = float('inf')
    else:
      diff_percentage = 100 * diff / abs(mean_a)
    is_probably_same = abs(diff_percentage) < 0.1 and not statistically_significant
    print mean_a, mean_b, t, statistically_significant, is_probably_same
    if is_probably_same:
        return 'SAME', statistically_significant
    if not statistically_significant:
        return 'FLAKY', statistically_significant
    if abs(diff_percentage) < 1:
        return 'SAME?', statistically_significant
    if (bigger_is_better and diff > 0) or (not bigger_is_better and diff < 0):
        return 'GOOD', statistically_significant
    return 'BAD', statistically_significant

def find_json_files(directory):
  for root, dirs, files in os.walk(directory):
    for basename in files:
      if fnmatch.fnmatch(basename, '*.json'):
        filename = os.path.join(root, basename)
        yield filename

def load_benchmark_results(dir):
  benchmark_set = {}
  json_files = find_json_files(dir)
  for file in json_files:
    f = open(file, 'r')
    try:
      o = json.load(f)
    except ValueError:
      continue
    benchmark_name = o['benchmark_name']
    for page in o['per_page_values']:
      test_name = '%s/%s' % (benchmark_name, page['name'])
      if test_name not in benchmark_set:
        benchmark_set[test_name] = {
          'units': page['units'],
          'values': []
        }
      if page['type'] == 'list_of_scalar_values':
        benchmark_set[test_name]['values'].extend(page['values'])
      elif page['type'] == 'scalar':
        benchmark_set[test_name]['values'].append(page['value'])
      else:
          continue
  return benchmark_set

def main():
  usage = "usage: %prog [options] <baseline - directory containing json files> <actual - directory containing json files>"
  parser = optparse.OptionParser(usage)
  parser.add_option("-v", "--verbose", dest="verbose_mode",
                    action="store_true",
                    default=False,
                    help="print more info")
  parser.add_option("-o", "--output", dest="output",
                    default=None,
                    help="output csv file")
  options, args = parser.parse_args()

  if options.verbose_mode:
    logging.getLogger().setLevel(logging.INFO)
  
  if options.output is not None:
    output_file = os.path.abspath(options.output)
  else:
    (_, output_file) = tempfile.mkstemp()
  logging.info("Ouput file at %s", output_file)
  
  if len(args) < 2:
    logging.error('This requires two input directories. Only %d supplied.', len(args))
    parser.print_help()
    exit()
  
  baseline_data = load_benchmark_results(args[0])
  actual_data = load_benchmark_results(args[1])
  
  csvfile = open(output_file, 'w+b')
  writer = csv.writer(csvfile)
  writer.writerow(['test name', 'page name', 'units', 'summary', 'diff(%)', 'mean(baseline)', 'mean(actual)', 'stdev(baseline)', 'stdev(actual)', 'statistically significant', 'count(baseline)', 'count(actual)', 'min(baseline)', 'max(baseline)', 'min(actual)', 'max(actual)'])
  
  tests = set(baseline_data.keys()).intersection(actual_data.keys())
  tests = list(tests)
  tests.sort()
  for test_name in tests:
    a = baseline_data[test_name]['values']
    b = actual_data[test_name]['values']
    if len(a) == 0:
      logging.warning("baseline_data %s is empty", test_name)
      if len(b) == 0:
        logging.warning("actual_data %s is empty", test_name)
      continue
    if len(b) == 0:
      logging.warning("actual_data %s is empty", test_name)
      continue
    units = baseline_data[test_name]['units']
    bigger_is_better = lookup_bigger_is_better(units)
    mean_a = compute_mean(a)
    mean_b = compute_mean(b)
    std_dev_a = compute_std_dev(a)
    std_dev_b = compute_std_dev(b)
    diff = mean_b - mean_a;
    if not bigger_is_better:
      diff *= -1
    if mean_a == 0:
      diff_percentage = float('inf')
    else:
      diff_percentage = 100 * diff / abs(mean_a)
    summary, statistically_significant = compute_summary(a, b, bigger_is_better)
    test_name_parts = test_name.split('/')
    writer.writerow([test_name_parts[0], test_name_parts[1], units, summary, diff_percentage, mean_a, mean_b, std_dev_a, std_dev_b, statistically_significant, len(a), len(b), min(a), max(a), min(b), max(b)])

if __name__ == "__main__":
  sys.exit(main())

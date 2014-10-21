#!/bin/bash

while read test_name; do
  $CHROMIUM_DIR/src/tools/perf/run_benchmark run --browser=release $test_name --output-format=json --output-dir ~/bench-master-oilpan --page-repeat=10
done < benchmarks.txt

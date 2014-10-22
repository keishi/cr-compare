#!/bin/bash

while read test_name; do
  $CHROMIUM_DIR/src/tools/perf/run_benchmark run --browser=release $test_name --output-format=json --output-dir $1/$test_name --page-repeat=10
done < `dirname $0`/benchmarks.txt

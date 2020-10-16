#!/bin/bash

if [ ! -d ./sparkle-midpoint-cov ]; then
	echo "Integartion tests coverage files not generated, skipping"
	exit 0
fi

mkdir it-cov

ls ./sparkle-midpoint-cov

for f in `ls ./sparkle-midpoint-cov`; do
	mkdir tmp
	tar -C ./tmp -xvf ./sparkle-midpoint-cov/$f
	cp ./tmp/.coverage ./it-cov/.coverage_$f
	rm tmp -rf
done

cd it-cov
coverage report -m
coverage html


#!/bin/bash

if [ ! -d ./sparkle-midpoint-cov ]; then
	echo "Integration tests coverage files not generated, skipping"
	exit 0
fi

mkdir it-cov

for f in `ls ./sparkle-midpoint-cov`; do
	mkdir tmp
	tar -C ./tmp -xvf ./sparkle-midpoint-cov/$f
	cp ./tmp/.coverage ./it-cov/.coverage.`echo $f | cut -d '.' -f1`
	rm tmp -rf
done

cd it-cov
ln -s src ../src

../venv/bin/coverage combine
../venv/bin/coverage report -m -i
../venv/bin/coverage html -i


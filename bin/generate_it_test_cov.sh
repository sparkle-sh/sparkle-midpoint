#!/bin/bash

if [ ! -d ./sparkle-midpoint-cov ]; then
	echo "Integration tests coverage files not generated, skipping"
	exit 0
fi

mkdir it-cov
sudo ln -s . /sparkle-midpoint
pushd /sparkle-midpoint/

for f in `ls ./sparkle-midpoint-cov`; do
	mkdir tmp
	tar -C ./tmp -xvf ./sparkle-midpoint-cov/$f
	cp ./tmp/.coverage ./it-cov/.coverage.`echo $f | cut -d '.' -f1`
	rm tmp -rf
done

cd it-cov
../venv/bin/coverage combine --append
mv .coverage ..
cd ..

./venv/bin/coverage report -m
./venv/bin/coverage html

mv ./htmlcov it-cov


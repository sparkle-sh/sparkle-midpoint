#!/bin/bash

cd ./logs
mkdir tmp

for l in `ls *.tar`; do
	tar -C ./tmp -xvf ./$l
	mv ./tmp/sparkle-midpoint.log ./`echo $l | cut -d '.' -f1-3`.log
done

rm *.tar
rm -rf tmp

cd ..
ls ./logs



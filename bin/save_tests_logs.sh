#!/bin/bash

cd ./logs
mkdir tmp

for l in `ls *.tar`; do
	tar -C ./tmp -xvf ./$l
	mv ./tmp/sparkle-midpoint.log ./`echo $f cut -d '.tar' -f1`.log
done

rm *.tar
rm tmp -f

cd ..
ls ./logs



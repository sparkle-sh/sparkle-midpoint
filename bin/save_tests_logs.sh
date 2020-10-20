#!/bin/bash

cd ./logs
mkdir tmp

for l in `ls *.tar`; do
	tar -C ./tmp -xvf ./$l
done

rm *.tar
cp ./tmp/* .
rm tmp

cd ..
ls ./logs



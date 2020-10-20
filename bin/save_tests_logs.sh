#!/bin/bash

cd ./logs
mkdir tmp

for l in `ls ./tmp/*.tar`; do
	tar -C ./tmp -xvf ./$f
done

rm *.tar
cp ./tmp/* .
rm tmp

cd ..
ls ./logs



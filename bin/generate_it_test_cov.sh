#!/bin/bash

if [ ! -d ./sparkle-midpoint-cov ]; then
	echo "Test coverage files not generated, skipping"
	exit 0
fi



#!/bin/bash
for i in {01..10}; do
	docker kill ot_$i
done

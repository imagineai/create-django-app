#!/bin/bash
sed -i.bak '13s/.*/    server: '$1'/' $2

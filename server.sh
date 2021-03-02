#!/bin/bash
sed -i.bak '15s/.*/    server: '$1'/' $2

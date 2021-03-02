#!/bin/bash
sed -i.bak '13s/.*/    package-manager: '$1'/' $2

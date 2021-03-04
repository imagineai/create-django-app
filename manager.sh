#!/bin/bash
sed -i.bak '11s/.*/    package-manager: '$1'/' $2

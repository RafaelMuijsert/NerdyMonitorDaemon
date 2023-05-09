#!/bin/bash

used=$(df --total | grep ^total | awk '{ print $3 }')
available=$(df --total | grep ^total | awk '{ print $4 }')
use_percent=$(df --total | grep ^total | awk '{ print $5 }')

echo "$used used (${use_percent}), ${available} available "

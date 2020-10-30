#!/bin/bash
Pid=$(ps -elf | grep main.py | grep -v grep | awk '{print $4}')
kill ${Pid}
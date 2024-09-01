#! /usr/bin/env bash
export PS1='\[\033[01;91m\]($name)\[\033[00m\] \[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
sysctl vm.overcommit_memory=1
redis-server --daemonize yes

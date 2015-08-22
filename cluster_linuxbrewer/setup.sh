#!/bin/bash

#############User Definition Start##################
export HOME=/panfs/cmb-panasas2/skchoudh/software_frozen/brew
#############User Definition End##################


#############Do NOT edit#################
# Ideally the settings below should not require editing

export cache=~/.cache
export LINUXBREWUSER=$(whoami)
export HOMEBREW_HOME=$HOME/linuxbrew
export software=$HOME/software
export PATH=$HOMEBREW_HOME/bin:$software/bin:$PATH
export scratch=$software/scratch
export brewcache=$HOME/linuxbrew_cache
export HOMEBREW_BUILD_FROM_SOURCE=1
export HOMEBREW_CC=gcc
#############Do NOT Edit##################

#!/bin/bash
# Script to install linuxbrew on cluster 
# with few other packages required desperately

set -e

#############User Defined##################
export HOME=/path/to/downloadlocation
export brewcache=$HOME/linuxbrew_cache
export cache=~/.cache
mpdir -p $brewcache
if [ -d "$cache" ]; then
  mv $cache/* $brewcache
  rm -rf $cache
fi
## Home is limisted to 1GB, insufficient to get going!
ln -s $brewcache $cache

###########################################

# Ideally the settings below should not require editing

export LINUXBREWUSER=$(whoami)
export HOMEBREW_HOME=$HOME/linuxbrew
export software=$HOME/software
export PATH=$HOMEBREW_HOME/bin:$software:$PATH
export scratch=$software/scratch
export HOMEBREW_BUILD_FROM_SOURCE=1

mkdir -p $software
mkdir -p $scratch && cd $scratch

wget -c http://pyyaml.org/download/libyaml/yaml-0.1.5.tar.gz
tar -zxvf yaml-0.1.5.tar.gz
cd yaml-0.1.5
./configure --prefix=$software
make && make install

cd $scratch

##Ruby
wget -c http://cache.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p547.tar.gz
tar -zxvf ruby-1.9.3-p547.tar.gz 
cd ruby-1.9.3-p547
./configure --prefix=$software --disable-install-doc --with-opt-dir=$software
make && make install

rm -rf $scratch

cd $HOME
git clone https://github.com/Homebrew/linuxbrew.git linuxbrew
mkdir linuxbrew/lib
( cd linuxbrew; ln -s lib $HOMEBREW_HOME/lib64 )

ln -s /usr/lib64/libstdc++.so.6 /lib64/libgcc_s.so.1 $HOMEBREW_HOME/lib/
brew install glibc
brew unlink glibc
brew install https://raw.githubusercontent.com/Homebrew/homebrew-dupes/master/zlib.rb
brew reinstall binutils
brew link glibc
brew install gcc --with-glibc -v
rm -f $HOMEBREW_HOME/lib/{libstdc++.so.6,libgcc_s.so.1}
brew link gcc
export HOMEBREW_CC=gcc-4.9

brew install curl expat git
brew tap homebrew/dupes
brew tap homebrew/science
brew install libxml2 python
brew install bzip2 coreutils findutils gawk gnu-sed gnu-which grep libpng libxml2 libxslt make ncurses readline 

##Ncurses hacks
#ln -s $HOMEBREW_HOME/Cellar/ncurses/5.9/include/ncursesw/* $HOMEBREW_HOME/include/
#ln -s $HOMEBREW_HOME/Cellar/ncurses/5.9/lib/libncurses.so $HOMEBREW_HOME/lib/libncurses.so
#ln -s $HOMEBREW_HOME/Cellar/ncurses/5.9/lib/libncurses.so $HOMEBREW_HOME/lib/libcurses.so
ln -s $HOMEBREW_HOME/Cellar/ncurses/5.9/include/ncursesw/curses.h $HOMEBREWHOME/Cellar/ncurses/5.9/include/ncursesw/ncurses.h ncursesw/termcap.h $HOMEBREW_HOME/include/
brew install bwa samtools tophat bowtie bowtie2 bwa sratoolkit methpipe


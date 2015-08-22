#!/bin/bash
# Script to install linuxbrew on cluster 
# with few other packages required desperately

set -ex



#####Setup#######
source ${PWD}/setup.sh

rm -rf $brewcache
mkdir -p $brewcache
if [ -d "$cache" ] && [ "$(ls -A $cache)" ]; then
  mv $cache/* $brewcache
  rm -rf $cache
fi
## Home is limisted to 1GB, insufficient to get going!
ln -s $brewcache $cache
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
rm -rf linuxbrew
git clone --depth 1 --branch master https://github.com/Homebrew/linuxbrew.git linuxbrew
mkdir linuxbrew/lib
( cd linuxbrew; ln -s lib $HOMEBREW_HOME/lib64 )

ln -s /usr/lib64/libstdc++.so.6 /lib64/libgcc_s.so.1 $HOMEBREW_HOME/lib/

##Symlink gcc

ln -s $(which gcc) $HOMEBREW_HOME/bin/gcc-$(gcc -dumpversion |cut -d. -f1,2)
ln -s $(which g++) $HOMEBREW_HOME/bin/g++-$(g++ -dumpversion |cut -d. -f1,2)
ln -s $(which gfortran) $HOMEBREW_HOME/bin/gfortran-$(g++ -dumpversion |cut -d. -f1,2)

brew install glibc
brew unlink glibc
brew install https://raw.githubusercontent.com/Homebrew/homebrew-dupes/master/zlib.rb
brew reinstall binutils
brew link glibc
brew install gcc --with-glibc
rm -rf $HOMEBREW_HOME/lib/libstdc++.so.6
rm -rf $HOMEBREW_HOME/lib/libgcc_s.so.1

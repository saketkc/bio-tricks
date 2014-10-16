#!/usr/bin/bash
## Install linuxbrew on cluster x86_64[login2]

set -e

export LINUXBREWUSER=skchoudh
export LINUXBREWHOME=/home/cmb-06/as/$LINUXBREWUSER/linuxbrew
export PATH=$LINUXBREWHOME/bin:/home/cmb-06/as/skchoudh/software_frozen/bin:$PATH

export myhome=/home/cmb-06/as/$LINUXBREWUSER
export scratch=$myhome/scratch
export software=/home/cmb-06/as/$LINUXBREWUSER/software_frozen

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

cd $myhome
git clone https://github.com/Homebrew/linuxbrew.git linuxbrew
mkdir linuxbrew/lib
( cd linuxbrew; ln -s lib lib64 )

ln -s /usr/lib64/libstdc++.so.6 /lib64/libgcc_s.so.1 $LINUXBREWHOME/lib/
brew install glibc
brew unlink glibc
brew install https://raw.githubusercontent.com/Homebrew/homebrew-dupes/master/zlib.rb
brew reinstall binutils
brew link glibc
brew install gcc --with-glibc -v
rm -f $LINUXBREWHOME/lib/{libstdc++.so.6,libgcc_s.so.1}
brew link gcc
export HOMEBREW_CC=gcc-4.9

brew install curl expat git
brew tap homebrew/dupes
brew tap homebrew/science
brew install python
brew install bzip2 coreutils findutils gawk gnu-sed gnu-which grep libpng libxml2 libxslt make readline 
brew install r samtools tophat bowtie bowtie2 bwa sratoolkit



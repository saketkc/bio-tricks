#!/bin/bash
source ${PWD}/setup.sh


rm -rf $HOMEBREW_HOME/lib/libstdc++.so.6
rm -rf $HOMEBREW_HOME/lib/libgcc_s.so.1
brew link --overwrite gcc
brew install hello && brew test hello; brew remove hello

brew install curl expat git
brew tap homebrew/dupes
brew tap homebrew/science
brew install libxml2 python
brew install bzip2 coreutils findutils gawk gnu-sed gnu-which grep libpng libxml2 libxslt make ncurses readline ruby

##Ncurses hacks
ln -s $HOMEBREW_HOME/Cellar/ncurses/5.9/include/nncursesw/curses.h ncursesw/form.h ncursesw/ncurses.h ncursesw/term.h ncursesw/termcap.h $HOMEBREW_H$
ln -s $HOMEBREW_HOME/Cellar/ncurses/5.9/lib/libncurses.so $HOMEBREW_HOME/lib/libcurses.so
ln -s $HOMEBREW_HOME/Cellar/ncurses/5.9/lib/libncurses.a $HOMEBREW_HOME/lib/libcurses.a

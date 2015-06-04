#!/usr/bin/env
import os
import shutil
import sys
import fnmatch


__destination_path__ = '/media/data1/ENCODE/plots_with/'

def recursive_rename(argv):
    arg = argv[0]
    matches = []
    for root, dirnames, filenames in os.walk(arg):
        for filename in fnmatch.filter(filenames, r'*_scatter.png') + fnmatch.filter(filenames, r'*_trend.png'):
            fs = filename.split('_')
            control = ''
            if 'Control' in root:
                control = 'Control'
            renamed = ('_').join(filename.split('_')[3:])
            renamed = renamed[:6]+ '_' + fs[0] + renamed[6:]
            directory = os.path.join(__destination_path__, root.split('/')[4], control)
            source = os.path.join(root, filename)
            destination = os.path.join(directory, renamed)
            matches.append(source)
            if not os.path.exists(directory):
                os.makedirs(directory)
            shutil.copy(source, destination)

if __name__ == '__main__':
    recursive_rename(sys.argv[1:])

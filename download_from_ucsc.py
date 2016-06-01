import sys
from ftplib import FTP
def recursive_download(url):

    ftp = FTP('hgdownload.cse.ucsc.edu')
    ftp.login('anonymous', 'user@gmail.com')
    cwd = url.replace('http://hgdownload.cse.ucsc.edu/', '')
    ftp.cwd(cwd)
    filenames = ftp.nlst()
    print filenames
    for filename in filenames[2:]:
        f = open(filename, 'wb')
        ftp.retrbinary('RETR ' + filename, f.write)
        f.close()

if __name__ == '__main__':
    recursive_download(sys.argv[1])

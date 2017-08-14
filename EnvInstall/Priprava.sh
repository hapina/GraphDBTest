# !/bin/bash
#
# Priprava prostredi - custom
#

# Dropbox
cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86" | tar xzf -
alias dropbox-start=~/.dropbox-dist/dropboxd


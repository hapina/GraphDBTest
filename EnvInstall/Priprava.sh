# !/bin/bash
#
# Priprava prostredi - custom
#

# git
sudo apt-get update
sudo apt-get install git

# key add to github
#cd ~/.ssh
#ssh-keygen


# create a new repository
#echo "# graphtest" >> README.md
#git init
#git add README.md
#git commit -m "first commit"
#git config --global user.name "hapina"
#git config --global user.email radka.karvankova@gmail.com
#git commit --amend --reset-author

# push an existing repository
git remote add origin git@github.com:hapina/graphtest.git
git push -u origin master

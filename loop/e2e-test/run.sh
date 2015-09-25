#!/bin/bash

PATH_MARIONETTE="$PWD/tests/marionette/marionette"
#PATH_FIREFOX="/Applications/Firefox.app/Contents/MacOS"
PATH_FIREFOX="$PWD/firefox"
PATH_INI="$PWD/caller_case.ini"
VENV_BIN="$PWD/marionette_env/bin"

echo
echo "------------------------------------------------"
echo "VIRTUALENV"
echo "------------------------------------------------"
echo

virtualenv marionette_env
. $PWD/marionette_env/bin/activate 
$VENV_BIN/pip install marionette_client six pexpect pyperclip mozdownload
sudo apt-get install xclip

echo
echo "------------------------------------------------"
echo "DOWNLOAD FIREFOX"
echo "------------------------------------------------"
echo

# [1]. download Firefox
# TODO: figure out downloading: Nightly, Beta, etc.
$VENV_BIN/mozdownload --version=latest
rm -rf firefox
tar xjfv *.bz2

echo
echo "------------------------------------------------"
echo "DOWNLOAD MARIONETTE TESTS"
echo "------------------------------------------------"
echo

# [2]. download common.tests.zip
$VENV_BIN/mozdownload --type=daily --extension=common.tests.zip
# xclip needed for ubuntu
# [4]. mkdir tests
rm -rf tests;
mkdir tests

# [5]. unzip common.tests.zip in ./tests dir
cp *common.tests.zip tests
unzip  *common.tests.zip -d tests

echo
echo "------------------------------------------------"
echo "RUN TEST"
echo "------------------------------------------------"
echo

#$VENV_BIN/python "$PATH_MARIONETTE/runtests.py" --binary="$PATH_FIREFOX/firefox-bin" --address=localhost:2828 --type=browser $PATH_INI 
python "$PATH_MARIONETTE/runtests.py" --binary="$PATH_FIREFOX/firefox-bin" --address=localhost:2828 --type=browser $PATH_INI 



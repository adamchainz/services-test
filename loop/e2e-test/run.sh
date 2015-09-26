#!/bin/bash

PATH_MARIONETTE="$PWD/tests/marionette/marionette"
VENV_BIN="$PWD/marionette_env/bin"
if [ -z "$1" ]; then
   # we'll do this by default, but if no arg supplied
   # we could instead run them all
   TEST_NAME="loop_fxa_contact_call"
else
   TEST_NAME="$1"
fi
PATH_INI="$PWD/$TEST_NAME.ini"

echo
echo "------------------------------------------------"
echo "VIRTUALENV"
echo "------------------------------------------------"
echo

virtualenv marionette_env
. $PWD/marionette_env/bin/activate 
$VENV_BIN/pip install marionette_client six pexpect pyperclip mozdownload

echo "----------------------------------"
echo "INSTALL FIREFOX: $OSTYPE"
echo "----------------------------------"
echo
if [[ "$OSTYPE" == "linux-gnu" ]]; then

    echo "SET FIREFOX BIN PATH"
    PATH_FIREFOX="$PWD/firefox"
    echo $PATH_FIREFOX

    echo "INSTALL LINUX DEPS"
    sudo apt-get install xclip

    echo "DOWNLOAD FIREFOX"
    $VENV_BIN/mozdownload --version=latest

    echo "CLEANUP"
    rm -rf firefox
    tar xjfv *.bz2

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "SET FIREFOX BIN PATH"
    # TODO: mount new dmg, hard-coding to existing for now
    PATH_FIREFOX="/Applications/Firefox.app/Contents/MacOS"
    echo $PATH_FIREFOX
else
    echo "don't recognize OS... ABORTING!"
    exit
fi

echo
echo "------------------------------------------------"
echo "DOWNLOAD MARIONETTE TESTS"
echo "------------------------------------------------"
echo

$VENV_BIN/mozdownload --type=daily --extension=common.tests.zip
rm -rf tests;
mkdir tests

cp *common.tests.zip tests
unzip  *common.tests.zip -d tests

echo "CLEANUP"
rm *common.tests.zip

echo
echo "------------------------------------------------"
echo "RUN TEST"
echo "------------------------------------------------"
echo

$VENV_BIN/python "$PATH_MARIONETTE/runtests.py" --binary="$PATH_FIREFOX/firefox-bin" --address=localhost:2828 --type=browser $PATH_INI 
#python "$PATH_MARIONETTE/runtests.py" --binary="$PATH_FIREFOX/firefox-bin" --address=localhost:2828 --type=browser $PATH_INI 

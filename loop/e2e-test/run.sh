#!/bin/bash

SKIP_INSTALL="$2"
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
PATH_MARIONETTE="$DIR/tests/marionette/marionette"
VENV_BIN="$DIR/marionette_env/bin"

if [ -z "$1" ]; then
   # we'll do this by default, but if no arg supplied
   # we could instead run them all
   TEST_NAME="loop_fxa_contact_call"
else
   TEST_NAME="$1"
fi
PATH_INI="$DIR/$TEST_NAME.ini"

echo
echo "------------------------------------------------"
echo "VIRTUALENV"
echo "------------------------------------------------"
echo

if [ -z "$SKIP_INSTALL" ]; then
    virtualenv marionette_env
fi
. $DIR/marionette_env/bin/activate 

if [ -z "$SKIP_INSTALL" ]; then
    $VENV_BIN/pip install marionette_client six pexpect pyperclip mozdownload
fi

echo
echo "----------------------------------"
echo "INSTALL FIREFOX: OS=$OSTYPE"
echo "----------------------------------"
echo

if [[ "$OSTYPE" == "linux-gnu" ]]; then

    echo "SET FIREFOX BIN PATH"
    PATH_FIREFOX="$DIR/firefox"
    echo $PATH_FIREFOX

    if [ -z "$SKIP_INSTALL" ]; then
        echo "INSTALL LINUX DEPS"
        sudo apt-get install xclip

	echo "DOWNLOAD FIREFOX"
	$VENV_BIN/mozdownload --version=latest

	echo "CLEANUP"
	rm -rf firefox
	tar xjf *.bz2
    fi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "SET FIREFOX BIN PATH"
    # TODO: mount new dmg, hard-coding to existing for now
    PATH_FIREFOX="/Applications/Firefox.app/Contents/MacOS"
    echo $PATH_FIREFOX
else
    echo "don't recognize OS... ABORTING!"
    exit
fi

if [ -z "$SKIP_INSTALL" ]; then
    echo
    echo "------------------------------------------------"
    echo "DOWNLOAD MARIONETTE TESTS"
    echo "------------------------------------------------"
    echo

    $VENV_BIN/mozdownload --type=daily --extension=common.tests.zip
    rm -rf tests;
    mkdir tests

    cp *common.tests.zip tests
    unzip -q *common.tests.zip -d tests

    echo "CLEANUP"
    rm *common.tests.zip
fi

echo
echo "------------------------------------------------"
echo "RUN TEST"
echo "------------------------------------------------"
echo


#$VENV_BIN/python "$PATH_MARIONETTE/runtests.py" --binary="$PATH_FIREFOX/firefox-bin" --address=localhost:2828 --type=browser $PATH_INI 
python "$PATH_MARIONETTE/runtests.py" --binary="$PATH_FIREFOX/firefox-bin" --address=localhost:2828 --type=browser $PATH_INI 

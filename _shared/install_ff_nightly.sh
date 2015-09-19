#!/bin/bash

echo
echo Downloading latest Nightly...
echo  
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )


function install_ff_linux {
    echo "install linux"
    wget https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/latest/linux-x86_64/en-US/firefox-38.0.5.tar.bz2
    tar -xjvf *.bz2 -C $HOME/bin

}


function install_ff_darwin {

    # OSX
    rm -rf $DIR'/LatestNightly.dmg'


    LATEST_DMG=$(curl -s ftp://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-mozilla-central/ | fgrep en-US.mac.dmg | awk '{print $9}'
    )
    curl -# -C - -o $DIR'/LatestNightly.dmg' "ftp://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-mozilla-central/$LATEST_DMG"
    open $DIR'/LatestNightly.dmg'

    # TODO: Replace with monitor for download complete
    echo
    echo Waiting 20 seconds for disk image to be mounted...
    echo
    sleep 20
    echo mounting Firefox...
    cd /Volumes/Nightly/FirefoxNightly.app/Contents/MacOS
npm install

}

echo "----------------------------------"
echo "INSTALL OS-SPECIFIC: $OSTYPE"
echo "----------------------------------"
echo
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    install_ff_linux

elif [[ "$OSTYPE" == "darwin" ]]; then
    install_ff_darwin

else
    echo "don't recognize OS!"
    exit
fi

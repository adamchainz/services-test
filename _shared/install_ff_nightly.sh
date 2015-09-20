#!/bin/bash

echo  
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ROOT_URL="https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/latest"

function download {
    URL="$1"
    FILE=`curl -s "$URL/" | grep 'href' | sed 's/.*href="//' | sed 's/".*//' | grep '^[a-zA-Z].*' ` 
    echo "Downloading latest $OSTYPE Nightly: $FILE"
    curl -s -O $URL/$FILE
}

function install_ff_linux {
    PATH_OS="$ROOT_URL/linux-x86_64/en-US"
    echo $PATH_OS
    download $PATH_OS
    
    # launch here
    mkdir -p $HOME/bin
    rm -rf  $HOME/bin/*f
    tar xvjf ./$FILE -C $HOME/bin
    rm -f $FILE 
    $HOME/bin/firefox/firefox
}

function install_ff_darwin {
    PATH_OS="$ROOT_URL/mac/en-US"
    download $PATH_OS
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
echo "INSTALL FIREFOX: $OSTYPE"
echo "----------------------------------"
echo
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    install_ff_linux 

elif [[ "$OSTYPE" == "darwin" ]]; then
    install_ff_darwin

else
    echo "don't recognize OS... ABORTING!"
    exit
fi

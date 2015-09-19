LATEST="https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/latest/linux-x86-64/en-US/"
echo $LATEST

#curl "$LATEST"$(curl "$LATEST" 2>/dev/null | tail -1 | awk '{print $NF)}')

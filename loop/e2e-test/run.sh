echo $PWD
PATH_MARIONETTE="$PWD/tests/marionette/marionette"
PATH_FIREFOX="/Applications/Firefox.app/Contents/MacOS"
PATH_INI="$PWD/caller_case.ini"

# TODO: 
# [1]. download Firefox
# [2]. download common.tests.zip
# [3]. copy in STAGE prefs
# [4]. mkdir tests
# [5]. unzip common.tests.zip in ./tests dir
# -- look at firefox-ui-tests for setup examples (for handling ff downloads, prefs, etc.)

virtualenv marionette_env
. $PWD/marionette_env/bin/activate 
sudo pip install marionette_client six pexpect pyperclip

python "$PATH_MARIONETTE/runtests.py" --binary="$PATH_FIREFOX/firefox-bin" --address=localhost:2828 --type=browser $PATH_INI 

LOOP_SERVER_URL = "https://loop.services.mozilla.com"
FIREFOX_PREFERENCES = {
    "loop.server": LOOP_SERVER_URL + "/v0",
    "browser.dom.window.dump.enabled": True,
    # Some more changes might be necesarry to have this working in offline mode
    "media.peerconnection.use_document_iceservers": False,
    "media.peerconnection.ice.loopback": True,
    "devtools.chrome.enabled": True,
    "devtools.debugger.prompt-connection": False,
    "devtools.debugger.remote-enabled": True,
    "media.volume_scale": "0",
    "loop.gettingStarted.seen": True,
    "loop.seenToS": "seen",
    "loop.fxa_oauth.profile": "{\"email\":\"tryloopprod2@mailinator.com\",\"uid\":\"d9f6706f4f2844d1adc80d6dafaca094\",\"avatar\":\"https://firefoxusercontent.com/ffa03d588e46cf14710bfb15a7b202f9\",\"displayName\":\"Johnny Quest\"}",
    "loop.fxa_oauth.tokendata": "{\"token_type\":\"bearer\",\"access_token\":\"5972d1a8e8e35d996481b07652e15b4f5b07704acfacd63349b4f37127d3722b\",\"scope\":\"profile\"}",

    # this dialog is fragile, and likely to introduce intermittent failures
    "media.navigator.permission.disabled": True,
    # Use fake streams only
    "media.navigator.streams.fake": True
}

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
    "loop.fxa_oauth.profile": "{\"email\":\"tryloopprod@mailinator.com\",\"uid\":\"246e2ec1ca134e0fa51776ff09a49ab9\"}",
    "loop.fxa_oauth.tokendata": "{\"token_type\":\"bearer\",\"access_token\":\"bca8d697ac066445ae91da4a0d11c58a9b2da83517acad9ef91387e6b57188eb\",\"scope\":\"profile\"}",

    # this dialog is fragile, and likely to introduce intermittent failures
    "media.navigator.permission.disabled": True,
    # Use fake streams only
    "media.navigator.streams.fake": True
}

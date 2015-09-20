module.exports = {
  profile: {
    prefs: {
      'browser.startup.homepage': 'https://www.mozilla.org/en-US/firefox/hello/',
      'browser.feeds.showFirstRunUI': false,
      'browser.shell.checkDefaultBrowser': false,
      'browser.uitour.enabled': false,
      'devtools.chrome.enabled': true,
      'devtools.debugger.remote-enabled': true,
      'browser.startup.homepage': 'https://www.mozilla.org/en-US/firefox/hello/',
      'loop.server': 'https://loop.stage.mozaws.net/v0',
      'identity.fxaccounts.auth.uri': 'https://api-accounts.stage.mozaws.net',
      'identity.fxaccounts.remote.force_auth.uri': 'https://accounts.stage.mozaws.net/force_auth?service=sync&context=fx_desktop_v1',
      'identity.fxaccounts.remote.signin.uri': 'https://accounts.stage.mozaws.net/signin?service=sync&context=fx_desktop_v1',
      'identity.fxaccounts.remote.signup.uri': 'https://accounts.stage.mozaws.net/signup?service=sync&context=fx_desktop_v1',
      'identity.fxaccounts.remote.oauth.uri': 'https://oauth.accounts.stage.mozaws.net/v1',
      'identity.fxaccounts.remote.profile.uri': 'https://profile.accounts.stage.mozaws.net/v1',
      'identity.fxaccounts.remote.webchannel.uri': 'https://accounts.stage.mozaws.net/',
      'identity.fxaccounts.setting.uri': 'https://accounts.stage.mozaws.net/settings',
      'browser.dom.window.dump.enabled': true,
      'media.peerconnection.use_document_iceservers': false,
      'media.peerconnection.ice.loopback': true,
      'devtools.chrome.enabled': true,
      'devtools.debugger.prompt-connection': false,
      'devtools.debugger.remote-enabled': true,
      'media.volume_scale': '0',
      'loop.gettingStarted.seen': true,
      'loop.seenToS': 'seen',
      'media.navigator.permission.disabled': true,
      'media.navigator.streams.fake': true,
    }
  },
  desiredCapabilities: {
    raisesAccessibilityExceptions: false
  }
};

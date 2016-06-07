import ConfigParser
import pytest

from firefox_puppeteer import Puppeteer
from marionette_driver.marionette import Marionette
TIMEOUT = 20


def pytest_addoption(parser):
    """Options to be passed in at run time"""
    parser.addoption(
        "--env",
        action="store",
        help="choose a test environment: staging or production"
    )
    parser.addoption(
        "--bin",
        default='/Applications/FirefoxBeta.app/Contents/MacOS/firefox-bin',
        help='Path for Firefox binary'
    )


@pytest.fixture
def conf():
    config = ConfigParser.ConfigParser()
    config.read('manifest.ini')
    return config


@pytest.fixture
def env(request):
    return request.config.getoption("--env")


@pytest.fixture
def marionette(request, timeout):
    # Return a marionette instance
    m = Marionette(bin=request.config.option.bin)
    m.start_session()
    request.addfinalizer(m.delete_session)
    m.set_search_timeout(timeout)
    return m


@pytest.fixture
def puppeteer(marionette):
    puppeteer = Puppeteer()
    puppeteer.marionette = marionette
    puppeteer.prefs.set_pref('devtools.chrome.enabled', True)
    puppeteer.prefs.set_pref('ui.popup.disable_autohide', True)
    return puppeteer


@pytest.fixture
def firefox(puppeteer):
    firefox = puppeteer.windows.current
    with puppeteer.marionette.using_context(
            puppeteer.marionette.CONTEXT_CHROME):
        firefox.focus()
    puppeteer.marionette.set_context(puppeteer.marionette.CONTEXT_CONTENT)
    return firefox


@pytest.fixture
def timeout():
    return TIMEOUT


@pytest.fixture
def install_addons(marionette, request):
    from marionette_driver.addons import Addons
    addons = Addons(marionette)
    addons.install(request.config.option.addon)
    marionette.restart()


@pytest.fixture
def admin_url(request):
    return request.config.getoption("--admin-url")

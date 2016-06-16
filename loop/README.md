# Tests for Loop

##General Configuration

It's highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/)
in order to have an isolated environment.

From /loop

1. `virtualenv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

Verify that the `manifest.ini` file contains expected values since the tests
rely on using it for assertions.

## Configuration Check Tests

These tests are to be run whenever a deployment of loop happens. They access
the server via HTTP calls to health check and status end points. Then the
results are compared to known expected values.

The tests are using [pytest](http://pytest.org/latest/) so to run them do the
following:

`py.test -v -s --env=<environment> --server=version=<version> config-check/`

Where `<environment>` is `staging` or `production` and `<version>` is the
version of loop server that is deployed to the environment you are testing
against.

## E2E Tests

Tests in this directory are designed to test UI features of Loop. They require
the use of Firefox with Marionette support built-in, which is Firefox 46 and
above.

These tests are currently designed to be run manually. Development work was
done on Mac OS-X El Capitan so the location of the browser in the configuration
file will need to change.

The tests are using [pytest](http://pytest.org/latest/) so to run them do the
following:

`py.test -v --env=<environment> e2e-test/`

where `<environemt>` is one of `stage` or `prod`.

The tests start up a Firefox browser and run some automated tests. There might
be a manual step of telling the browser you wish to share your camera and
microphone.

After each test run be sure to close the browser or Marionette will complain
that it cannot make a connection on the correct port.

A generic client library and command line client for Pyjojo, which lives
[here](https://github.com/atarola/pyjojo). Together, they are
[Mojojojo](http://i.imgur.com/TW2EiMb.gif)!

## Important Note

Pyjojo implemented some
[breaking changes](https://github.com/atarola/pyjojo#recent-breaking-changes)
recently. This version of Pymojo, v0.8.x, is the first version that supports
versions of Pyjojo after these changes. As of v0.8.3, Pymojo is compatible with
both new and old versions of Pyjojo.

## Installation

    pip install pymojo

## Usage

### Command Line Client

In brief, for a totally default Jojo...

List the Jojo's scripts by name:

    mojo list

Show details on a script called "echo":

    mojo show echo

Run the "echo" script:

    mojo run echo text='Hello, world!'

Reload the Jojo's script listing:

    mojo reload

More officially, mojo works like this...

    mojo [-h] [-c CONFIG] [-e ENDPOINT] [-g GROUP] [-p PORT] [-s] [-i]
                [-u USER] [-w PASSWORD] [-n ENV] [-b {and,or,not}] [-t TAGS]
                {list,show,run,reload} [script] ...
    
    Mojo command line client
    
    positional arguments:
      {list,show,run,reload}
                            The action you want to take
      script                For 'show' and 'run' commands, this is the relevant
                            script
      params                Params to pass through the 'run' command in
                            'key1=value' format
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            A YAML configuration file
      -e ENDPOINT, --endpoint ENDPOINT
                            The host to connect to a Jojo instance on
      -g GROUP, --group GROUP
                            The group of Jojo instances to perform actions
      -p PORT, --port PORT  The port Jojo is listening on
      -s, --ssl             Use SSL
      -i, --ignore-warnings
                            Ignore SSL certificate security warnings
      -u USER, --user USER  The user to authenticate with
      -w PASSWORD, --password PASSWORD
                            The password to authenticate with
      -n ENV, --environment ENV
                            The name of the configured environment to control
      -b {and,or,not}, --list-boolean {and,or,not}
                            When listing with a script tag filter, this specifies
                            the boolean operator to use describing the tag filter.
      -t TAGS, --tags TAGS  When listing with a script tag filter, this specifies
                            the list of tags to filter by. Also see the -b flag.


The `show` and `run` actions require that you specify a `script` by name, which
you can discover with a `list`. The `run` action also optionally accepts a
series of key/value pairs to pass into said script as environment variables.
These should be written like this: `key1=value1 key2=value2`

#### Configuration

You can configure the command line client with YAML files defining connection
settings (using the options the library's constructor accepts). A sample
configuration might look like this:

    environments:
      local:
        endpoint: "localhost"
        port: 9090
        use_ssl: True
        verify: False
        user: localUserName
        password: l0calU$erP@ss
      bobs-jojo-server:
        endpoint: "192.168.1.201"
      steves-jojo-server:
        endpoint: "192.168.1.253"
    
    groups:
      jojos:
        - bobs-jojo-server
        - steves-jojo-server
      
    default_environment: "local"

That defines three environments, called "local", "bobs-jojo-server", and
"steves-jojo-server", whose settings can be used with the `-n` option, like so:

    mojo -n bobs-jojo-server list

If you don't provide a `-n` option, Mojo will try to use the
`default_environment`.

It also defines a group called "jojos" that targets both the "bobs-jojo-server"
and "steves-jojo-server" environments. This can be called up with the `-g`
option:

    mojo -g jojos list

Mojo will automatically pull in configration files found at `/etc/mojo.yml` and
`~/.mojo.yml`, but you can specify an additional config file with `-c`.
Configurations will be applied in the following order:

 1. `/etc/mojo.yml`, the global config file
 2. `~/.mojo.yml`, the user config file
 3. The optional custom config file defined with `-c`
 4. Connection options specified with other command line flags

If a config file does not define one of the constructor arguments defined in the
`Library` section below, the default value for that option will be used.

### Library

Mojo's constructor accepts the following arguments:

 * `endpoint` - The network path to the server. This should be an IP or domain.
   (default: "localhost")
 * `port` - The port Jojo listens on (default: 3000)
 * `use_ssl` - Whether or not to use HTTPS (default: False)
 * `verify` - Whether to bother verifying Jojo's SSL certificate (default: True)
 * `user` - The username for HTTP Basic Auth (default: None)
 * `password` - The password for HTTP Basic Auth (default: None)

So if all of those defaults are what you need, then getting your Mojo on is
quite simple indeed:

    from pymojo.mojo import Mojo

    mojo = Mojo()

As an example of using every last option Mojo's constructor accepts, here's how
to interact with a Jojo server running on `192.168.0.123:9090`, which uses a
self-signed SSL certificate and HTTP Basic Authentication...

    mojo = Mojo(endpoint="192.168.0.123", port=9090, use_ssl=True, verify=False,
                user="username", password="A good password")
    
Once you have a Mojo, it's easy to use:

    # Print a list of every script the Jojo knows about
    for s in mojo.scripts:
      print s

    # Get script details from Mojo's cache
    script = mojo.get_script("my_script")
    # script is now a JSON object detailing the remote script

    # Get script details, forcing a refresh of this data from the Jojo server
    script = mojo.get_script("my_script", False)
    # script is the script JSON data, and Mojo's cache has been updated

    # Get a list of scripts with the 'foo' or 'bar' tag
    scripts = mojo.get_scripts(param="any_tags", tags="foo,bar")
    # Get a list of scripts with both the 'foo' and 'bar' tags
    scripts = mojo.get_scripts(param="tags", tags="foo,bar")
    # Get a list of scripts with neither the 'foo' nor 'bar' tags
    scripts = mojo.get_scripts(param="not_tags", tags="foo,bar")
    
    # Just get the names of scripts with a 'foo' or 'bar' tag
    script_names = mojo.get_script_names(param="any_tags", tags="foo,bar")

    # Run a Jojo script
    resp = mojo.run("my_script", {foo:"bar", bar:"foo"})
    # resp is a requests response object from which you can gather a
    # resp.status_code and get the JSON body with resp.json()

    # Reload the Jojo's configuration and Mojo's cache
    mojo.reload()

## Extending Mojo

Pyjojo is merely a remote script execution engine, and is meant to be extended
to meet the needs of its users. As-is, Pymojo can act on any custom scripts on
a Jojo server, but the specifics of a Jojo deployment can be easily wrapped up
in a class that inherits a Mojo.

Realistically, you'll use Jojo for things like remote service control or
software deployments, but for the sake of example, let's say our Jojo server
only knows how to execute one script, `echo.sh`, which looks like this:

    #!/bin/bash
    
    # -- jojo --
    # description: echo
    # param: text - Text to echo
    # -- jojo --
    
    echo ${TEXT}
    exit 0

We'll make a special kind of Mojo built to run this echo script. We'll call it
an Echojo.

    class Echojo(Mojo):
      def __init__(self, **kwargs):
        Mojo.__init__(self, **kwargs)
      
      def echo(self, text):
        return self.run("echo", {"text" : text})

Simply put, it takes the same Jojo configuration options that Mojo takes,
and then passes them on to the superconstructor. The `echo` function passes
data through the superclass's `run` function and passes the result back up.

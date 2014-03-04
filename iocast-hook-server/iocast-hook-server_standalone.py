#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="platform management")
    parser.add_argument('--host', help="host", required=False, default="localhost")
    parser.add_argument('--port', help="port", required=False, default=80)
    parser.add_argument('--debug', help="enables debugging (boolean switch to trueI)", action='store_true', required=False, default=False)
    parser.add_argument('--virtualenv', help="sets the virtual env", required=False, default=None)
    
    args = parser.parse_args()
    
    if args.virtualenv:
        activate_this = os.path.expanduser("{virtualenv}/bin/activate_this.py".format(virtualenv=args.virtualenv))
        execfile(activate_this, dict(__file__=activate_this))

    import bottle
    from webapp import app

    bottle.debug(args.debug)
    bottle.run(app=app, host=args.host, port=args.port, quiet=False, reloader=True)




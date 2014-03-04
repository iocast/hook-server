#!/usr/bin/env python
import os, sys, json, argparse, bottle


from webapp import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="platform management")
    parser.add_argument('--host', help="host", required=False, default="localhost")
    parser.add_argument('--port', help="port", required=False, default=80)
    parser.add_argument('--debug', help="enables debugging (boolean switch to trueI)", action='store_true', required=False, default=False)
    
    args = parser.parse_args()
    
    bottle.debug(args.debug)
    bottle.run(app=app, host=args.host, port=args.port, quiet=False, reloader=True)




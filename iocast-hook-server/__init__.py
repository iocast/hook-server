#!/usr/bin/env python
import os, sys, json, argparse, bottle




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="platform management")
    parser.add_argument('-p', '--port', help="port", required=False, default=8000)
    parser.add_argument('-g', '--debug', help="enables debugging (boolean switch to trueI)", action='store_true', required=False, default=False)


    bottle.debug(args.debug)
    bottle.run(app=get_app(), host='localhost', port=args.port, quiet=False, reloader=True)

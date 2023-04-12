import argparse

from transfermarktparser.transfermarkt_parser import TransfermarktParser

if __name__ == "__main__":
    tfp = TransfermarktParser()
    arg_parser = argparse.ArgumentParser(description="This is the parser of football games from TransferMarkt.com")
    arg_parser.add_argument('mode', type=str, help='Determines in which mode the parser is launched (start | update)')
    args = arg_parser.parse_args()
    if args.mode.lower() == 'start':
        tfp.get(update_only=False)
    elif args.mode.lower() == 'update':
        tfp.get(update_only=True)
    else:
        print(f'Mode {args.mode} is not defined. Try again.')

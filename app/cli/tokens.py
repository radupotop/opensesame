import argparse

from app.backend.logging import get_logger
from app.api import init

log = get_logger('CLI')
storage, _, _ = init(with_ipt=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest='maincmd',
    )
    # Main commands
    add_tokens = subparsers.add_parser(
        'add',
        help='Add tokens',
    )
    rm_tokens = subparsers.add_parser(
        'rm',
        help='Remove tokens',
        aliases=['del'],
    )
    # Sub-commands
    add_tokens.add_argument(
        '--expires-days',
        type=int,
        help='Expires in number of days',
    )
    add_tokens.add_argument(
        '--reason',
        type=str,
        help='Reason for granting access',
    )
    args = parser.parse_args()
    log.info('Arguments: %s', args)
    if args.maincmd == 'add':
        ret = storage.add_token(args.expires_days, args.reason)
        log.info('Added token %s, expires=%s', *ret)

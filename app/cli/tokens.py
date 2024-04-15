import argparse
from uuid import UUID

from app.api import init
from app.backend.logging import get_logger

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
    check_tokens = subparsers.add_parser(
        'check',
        help='Check if token exists',
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
    # Check
    check_tokens.add_argument(
        'uuid',
        type=UUID,
        help='Token UUID',
    )
    args = parser.parse_args()
    log.info('Arguments: %s', args)
    if args.maincmd == 'add':
        ret = storage.add_token(args.expires_days, args.reason)
        log.info('Added token %s, expires=%s', *ret)
    if args.maincmd == 'check':
        tok = storage.verify_token(args.uuid)
        if tok:
            log.info(
                'Token Valid %s → %s, Reason: %s',
                tok.created,
                tok.expires or 'Unlimited',
                tok.reason,
            )
        else:
            log.info('Token NOT FOUND!')

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
        help='Generate a new token',
    )
    exp_tokens = subparsers.add_parser(
        'exp',
        help='Expire a token',
    )
    check_tokens = subparsers.add_parser(
        'check',
        help='Check if a token exists',
    )
    ### Sub-commands ###
    # Add sub-command
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
    # Check sub-command
    check_tokens.add_argument(
        'uuid',
        type=UUID,
        help='Token UUID to check',
    )
    # Expire sub-command
    exp_tokens.add_argument(
        'uuid',
        type=UUID,
        help='Token UUID to expire',
    )
    args = parser.parse_args()
    # log.info('Arguments: %s', args)
    # ADD
    if args.maincmd == 'add':
        ret = storage.add_token(args.expires_days, args.reason)
        log.info('Added token %s, expires=%s', *ret)
    # CHECK
    if args.maincmd == 'check':
        tok = storage.get_token(args.uuid)
        if tok and tok.is_valid:
            log.info(
                'Token Valid %s → %s, Reason: %s',
                tok.created,
                tok.expires or 'Unlimited',
                tok.reason,
            )
        elif tok:
            log.info(
                'Token Expired %s, Reason: %s',
                tok.expires,
                tok.reason,
            )
        else:
            log.info('Token NOT FOUND!')
    # EXPIRE
    if args.maincmd == 'exp':
        ret = storage.expire_token(args.uuid)
        log.info('Token is now expired=%s', ret)

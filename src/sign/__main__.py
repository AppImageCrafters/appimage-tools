import argparse

from sign.create import sign_appimage
from sign.verify import verify_signature


def main():
    parser = argparse.ArgumentParser(description="AppImage Signatures management tool")
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_verify = subparsers.add_parser('verify', help='verify help')
    parser_verify.add_argument("target", help="AppImage file")

    parser_sign = subparsers.add_parser('sign', help='sign help')
    parser_sign.add_argument("--key", help="Key to be used", required=True)
    parser_sign.add_argument("target", help="AppImage file")

    args = parser.parse_args()

    if args.command == 'verify':
        verify_signature(args.target)

    if args.command == 'sign':
        sign_appimage(args.key, args.target)


if __name__ == "__main__":
    main()

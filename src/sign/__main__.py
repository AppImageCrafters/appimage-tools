import argparse

from sign.verify import verify_signature


def main():
    parser = argparse.ArgumentParser(description="AppImage Signatures management tool")
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_verify = subparsers.add_parser('verify', help='verify help')
    parser_verify.add_argument("target", help="AppImage file")

    args = parser.parse_args()
    verify_signature(args.target)


if __name__ == "__main__":
    main()

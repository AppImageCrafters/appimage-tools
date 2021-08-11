import argparse

from sign.verify import verify_signature


def main():
    parser = argparse.ArgumentParser(description="AppImage Signatures management tool")

    parser.add_argument("target", help="AppImage file")
    args = parser.parse_args()

    verify_signature(args.target)


if __name__ == "__main__":
    main()

import os
import subprocess
import tempfile

from sign.common import read_signatures_offset, read_file_into_fifo, read_signatures


def check_appimage_signature(target, signature):
    # file chunks will be written here
    fifo_path = tempfile.NamedTemporaryFile().name
    os.mkfifo(fifo_path)

    key_path = tempfile.NamedTemporaryFile().name
    with open(key_path, "w") as key_file:
        key_file.write(signature["data"])

    args = [
        "gpg",
        "--verify",
        key_path,
        fifo_path,
    ]

    with subprocess.Popen(args) as _proc:
        limit = read_signatures_offset(target)
        read_file_into_fifo(target, fifo_path, limit)

    os.unlink(fifo_path)
    os.unlink(key_path)


def verify_signature(target):
    signatures = read_signatures(target)
    for signature in signatures:
        if signature["method"] == "gpg":
            check_appimage_signature(target, signature)
            continue

        print(f"Signature method not supported {signature['method']}")

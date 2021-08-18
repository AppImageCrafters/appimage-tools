import os
import subprocess
import tempfile

import bson

from sign.common import read_signatures_offset, read_file_into_fifo


def sign_appimage(key, target):
    signatures_offset = read_signatures_offset(target)
    _sign_bundle(target, key, signatures_offset)


def _sign_bundle(output_filename, keyid, signatures_offset):
    signature = _generate_bundle_signature_using_gpg(
        keyid, output_filename, signatures_offset
    )

    encoded_signatures = bson.dumps(
        {
            "signatures": [
                {
                    "method": "gpg",
                    "keyid": keyid,
                    "data": signature,
                }
            ]
        }
    )

    with open(output_filename, "r+b") as fd:
        fd.seek(signatures_offset, 0)
        fd.write(encoded_signatures)


def _generate_bundle_signature_using_gpg(keyid, filename, limit):
    # file chunks will be written here
    input_path = tempfile.NamedTemporaryFile().name
    os.mkfifo(input_path)

    # sign the file with out including the signatures section
    output_path = tempfile.NamedTemporaryFile().name

    # call gpg
    args = [
        "gpg",
        "--detach-sign",
        "--armor",
        "--default-key",
        keyid,
        "--output",
        output_path,
        input_path,
    ]

    with subprocess.Popen(args) as _proc:
        read_file_into_fifo(filename, input_path, limit)

    # read output
    with open(output_path, "rb") as output:
        signature = output.read().decode()

    os.unlink(output_path)
    os.unlink(input_path)
    return signature

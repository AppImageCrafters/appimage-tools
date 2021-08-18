import os
import subprocess
import tempfile

import bson

from sign.common import read_signatures_offset, read_file_into_fifo, read_signatures


def create_signature(key, target, append=True):
    signatures_offset = read_signatures_offset(target)
    signature = _generate_bundle_signature_using_gpg(
        key, target, signatures_offset
    )

    signatures = []
    if append:
        signatures = read_signatures(target) or []

    signatures.append({
        "method": "gpg",
        "keyid": key,
        "data": signature,
    })

    _write_signature(target, signatures, signatures_offset)


def _write_signature(target, signatures, offset):
    encoded_signatures = bson.dumps({"signatures": signatures})
    with open(target, "r+b") as fd:
        fd.seek(offset, 0)
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

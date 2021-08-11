import bson


def read_file_into_fifo(filename, fifo_path, limit):
    # read file contents up to limit
    with open(fifo_path, "wb") as input_pipe:
        chunk_size = 1024
        n_chunks = int(limit / chunk_size)
        with open(filename, "rb") as input_file:
            for chunk_id in range(n_chunks):
                input_pipe.write(input_file.read(chunk_size))

            final_chunk_size = limit - (n_chunks * chunk_size)
            if final_chunk_size != 0:
                input_pipe.write(input_file.read(final_chunk_size))

            input_pipe.close()


def read_signatures_offset(target):
    with open(target, "rb") as f:
        f.seek(0x420, 0)
        chunk = f.read(8)
        signature_offset = int.from_bytes(chunk, byteorder="little")
        return signature_offset


def read_signatures(target):
    with open(target, "rb") as f:
        f.seek(0x420, 0)
        chunk = f.read(8)
        signature_offset = int.from_bytes(chunk, byteorder="little")
        f.seek(signature_offset, 0)
        signature_data_raw = f.read()
        signature_data = bson.loads(signature_data_raw)
        return signature_data["signatures"]

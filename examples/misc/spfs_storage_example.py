import io
import os
import asyncio

from swarms_tools.storage.spfs import SpfsStorageClient


def _generate_in_memory_file(size_in_mb: int) -> io.BytesIO:
    mega_byte = 1_000_000
    file_io = io.BytesIO(os.urandom(size_in_mb * mega_byte))
    return file_io


def base_example():
    print("ipfs storage sync base example")
    client = SpfsStorageClient(timeout=None)

    file_name = "hello"
    value = b"world"

    cid = client.put(value, file_name=file_name)
    print("Got cid:", cid)
    value_from_ipfs = client.get(cid)

    assert value == value_from_ipfs
    print("Value match")

    # or through contextmanager
    with SpfsStorageClient(timeout=None) as client:
        cid = client.put(value, file_name=file_name)
        print("Got cid:", cid)
        value_from_ipfs = client.get(cid)

        assert value == value_from_ipfs
        print("Value match")
    print("")


async def base_async_example():
    print("ipfs storage async base example")
    client = SpfsStorageClient(timeout=None)

    file_name = "ahello"
    value = b"aworld"

    cid = await client.aput(value, file_name=file_name)
    print("Got cid:", cid)
    value_from_ipfs = await client.aget(cid)

    assert value == value_from_ipfs
    print("Value match")

    await client.close()

    # or through contextmanager
    with SpfsStorageClient(timeout=None) as client:
        cid = await client.aput(value, file_name=file_name)
        print("Got cid:", cid)
        value_from_ipfs = await client.aget(cid)

        assert value == value_from_ipfs
        print("Value match")
    print("")


async def example_with_big_file():
    print("ipfs storage async big file example")
    client = SpfsStorageClient(timeout=None)

    file_name = "bigfile"
    file_ = _generate_in_memory_file(100)

    cid = await client.aput(file_, file_name=file_name)
    print("Got cid from big:", cid)
    value_from_ipfs = await client.aget(cid)

    original = file_.getvalue()
    retrieved = value_from_ipfs

    print("Data matches:", original == retrieved)
    assert original == retrieved
    print("Value match")

    await client.close()


def main():
    base_example()
    asyncio.run(base_async_example())
    asyncio.run(example_with_big_file())


if __name__ == "__main__":
    main()

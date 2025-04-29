# Host-Based Attack: Disk Overload

import os
import time

def overload_disk(path='/tmp/io_test_file', size_mb=10, duration=30):
    end_time = time.time() + duration
    buffer = b'x' * 1024 * 1024

    with open(path, 'wb') as f:
        while time.time() < end_time:
            for _ in range(size_mb):
                f.write(buffer)
            f.flush()
            os.fsync(f.fileno())
            f.seek(0)

    os.remove(path)

if __name__ == "__main__":
    print("Starting Disk I/O Overload...")
    overload_disk()
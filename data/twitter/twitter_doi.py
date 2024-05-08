from mpi4py import MPI
from datetime import datetime
import json
import time
import os
import sys
import traceback

###
# This script preprocesses and extracts data from the 120GB twitter file from Spartan.
# It is to be executed on Spartan with a proper MPI setting
###


def get_doi(filename, rank, size, chunk_size):
    read_size = 0  # size of the file content read in bytes
    f = open(filename, "rb")
    f.seek(rank * chunk_size)
    dates = set()

    if rank == 0:
        with open(f"twitter-doi-segment-{rank}.txt", "a+") as file_segment:
            file_segment.write("[\n")

    while read_size < chunk_size:
        line_bytes = f.readline()
        if not line_bytes:
            break
        line = line_bytes.decode()
        trimmed_line = line.strip()[:-1]
        read_size += len(line_bytes)

        try:
            row = json.loads(trimmed_line)
            doc = row["doc"]

            if "includes" in doc:
                places = doc["includes"]["places"] if type(doc["includes"]) == dict else doc["includes"]
                for place in places:
                    if "melbourne" in place["full_name"].lower():
                        sentiment = doc["data"]["sentiment"] if "sentiment" in doc["data"] else 0.0
                        sentiment = sentiment["score"] if type(sentiment) == dict else sentiment
                        tweet_obj = {
                            "created_at": doc["data"]["created_at"],
                            "text": doc["data"]["text"],
                            "sentiment": sentiment,
                            "location": place["full_name"]
                        }

                        with open(f"twitter-doi-segment-{rank}.txt", "a+") as file_segment:
                            file_segment.write(f"{json.dumps(tweet_obj, default=str)},\n")

                        created_at = datetime.strptime(doc["data"]["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        dates.add(str(created_at.date()))

        except json.JSONDecodeError:
            pass
        except Exception as e:
            print("An unexpected error occurred:", e)
            traceback.print_exc()

    with open(f"twitter-doi-segment-{rank}.txt", "rb+") as file_segment:
        if rank == size - 1:
            file_segment.seek(-2, 2)
            file_segment.write(str.encode("\n]"))
        else:
            file_segment.seek(-1, 2)
        file_segment.truncate()

    f.close()
    return dates


def merge_sets(sets):
    for i in range(1, len(sets)):
        sets[0].update(sets[i])
    return sets[0]


def main(filename):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    file_size = os.path.getsize(filename)
    chunk_size = file_size // size

    start = time.time()

    # The remainder is to be done by the last process
    if rank == size - 1:
        chunk_size += file_size % size

    dates = get_doi(filename, rank, size, chunk_size)
    gathered_data = comm.gather(dates, root=0)
    gathered_start_time = comm.gather(start, root=0)

    if rank == 0:
        cmd = "cat "
        for i in range(size):
            cmd += f"twitter-doi-segment-{i}.txt "
        cmd += "> twitter-doi.json"
        os.system(cmd)

        dates = merge_sets(gathered_data)
        print(dates)

        end = time.time()
        start = min(gathered_start_time)
        print(f"Total time cost: {end - start}s")


main(sys.argv[1])

from typing import Callable

""" Generate unqiue ids for components """

def _id_tracker():
    ids = [-1]

    def next_id():
        ids[0] += 1
        return ids[0]

    return next_id


unique_id: Callable[[], int] = _id_tracker()


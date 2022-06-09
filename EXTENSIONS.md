I had to modify the test_write.py unit test slightly.

It assumes that load_neos and load_approaches will return tuples, and I already had some dependencies on these returning list objects. One of them gets sorted in place.

Somewhere around line 40 in test_write.py this:

    neos = tuple(load_neos(TEST_NEO_FILE))
    approaches = tuple(load_approaches(TEST_CAD_FILE))

became this:

    neos = list(load_neos(TEST_NEO_FILE))
    approaches = list(load_approaches(TEST_CAD_FILE))

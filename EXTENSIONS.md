I am surprised you would reject the whole project because I pointed out a pretty basic, very simple issue with one of the unit tests.

I mean, you have the original files in your github. Nevertheless, I put the originals back in my repository for you. I now recast the input as a list in my database function. It causes mysterious errors in the file_write.py unit test (it's more like the unit test crashes your database) if you aren't expecting this undocumented requirement that you expect tuples as input parameters for the database. Because this one unit test invokes the database differently than every other piece of code, for no reason at all.

The instructions also say to use NaN in the JSON where diameter is empty. NaN is NOT a valid type in JSON. Also that's not what your unit tests look for, so maybe straighten that bit out.

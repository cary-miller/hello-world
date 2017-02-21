Solution to the CampSpot programming challenge.

Prints to stdout the names of campsites that match the search range and gap
rules.
To run it at the command line:

# python challenge.py [json_filepath]

To run the tests:

# python tests.py

Test code does not use any test framework in the interests of simplicity and
minimizing imports.

Json input includes campsite reservations.   I decided to convert reservations
to openings so we can compare similar objects;  ie desired dates vs available
dates.  I am not certain that was the best decision but it gives a different
perspective on the problem and often a new perspective is illuminating.  An
opening is assumed to exist after the final reservation for a campsite.

I took a functional approach.  Started to write a class at one point but opted
not to do that.  Most of the code is devoted to date intervals so a first
crack at defining relevant objects might be something like

class Interval:
    def reservations_2_openings(self):
    def is_in(self, other):
    def gaps_left(self, other):

No thought given to scaling.   



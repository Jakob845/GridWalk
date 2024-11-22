The square class contains a string called id that is used to select or refer to the different squares in the grid.
It has a boolean called obstacle that is set to true if a square is an obstical and can't be walked upon.
It has another boolean called deadEnd that is checked in the function FindPath if it has already walked there and couldn't progress from there.

Theres is 30 obsticals randomized across all squares except for squares in the outer frame so that it wont be a case where obsticals 
block all paths.
FindPath first tries to walk towards the other side of the grid (to the left the way i built this).
If it can't it tries to step down to the square below it. If it cant it tries to walk up and than to the right if can do that.
It also checks in these steps so the next step is not already in the steps taken list.
If it get's stuck the squares around it is set to deadEnds the current step is set to the previous step from the list and the last
appended step is removed.
This repeats until it's on the opposit side and than it checks if it's above or below the end position or goal and tries to walk up 
or down towards it.
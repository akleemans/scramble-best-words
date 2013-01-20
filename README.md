scramble-best-words
===================

Finds the most valuable words for a boggle or scramble game. Can be run on a web server which supports Python.

# Run
To execute the file on a websever, call the file with parameter `grid` and the grid, for example

    scramble.py?grid=ERTHNRITREADSTEF


# Remarks
- Make sure to update write permission of `log.txt`.
- Neither the search algorithm nor the script itself is optimized, so be aware that its execution can put quite some load on your server

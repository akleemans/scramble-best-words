scramble-best-words
===================

Finds the most valuable words for a boggle or scramble game. Can be run on a web server which supports Python.

# Run
Upload the files on a webserver and call `index.html`.
The script will be called with the parameter `grid` and the letters, for example `scramble.py?grid=ERTHNRITREADSTEF`.

# Remarks
- Make sure to update write permission of `log.txt`, so the script can capture the requests
- Neither the search algorithm nor the script itself is optimized, so be aware that its execution can put quite some load on your server

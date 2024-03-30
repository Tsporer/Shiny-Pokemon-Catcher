This is a script to automatically catch shiny pokemon. It requires user input to work properly. 

# Step 1: Installation
Ensure you have an IDE, Python installed, and mGBA
### [VS Code download](https://code.visualstudio.com/download)
### [Python download](https://www.python.org/downloads/)
### [mGBA download](https://mgba.io/downloads.html)

# Step 2: Find a pokemon ROM
This script works with ROM hacks as well.
### [Pokemon Fire Red](https://archive.org/download/1636PokemonFireRedUSquirrels)
### [Check out ROM hacks here](https://www.pokecommunity.com/forums/rom-hacks-showcase.184/)

# Step 3: Adjust mGBA settings
Open mGBA. Go to Audio/Video -> Video layers -> disable background 3.
This is because most pokemon games have the background change (the grass and sky)
based on the system time. This messes up color calculations, so background 3
must be disabled during the shiny detection process.

# Step 4: Use shiny.py
Make a file and copy and paste the contents from shiny.py into that file. 

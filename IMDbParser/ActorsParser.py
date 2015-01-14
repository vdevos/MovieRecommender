__author__ = 'Thom Hurks'

import os
import re

actorsFileName = "actors-converted-small.list"
outputFileName = "actors"
outputExtension = ".csv"

lineCounter = 0
# Useless IMDb header
headerOffset = 239

# Titles cannot start with a double quote, else it's a tv episode.
re_movie_title = re.compile("^[^\"].+(?:\((?:\d{4}|\?{4})/?[IXV]*\)|\{.+\})")
re_role = re.compile("\[(.+)\]")
# After the "------" pattern there is only nonsense.
re_eof = re.compile("^-+$")

if os.path.isfile(actorsFileName):
    with open(actorsFileName) as actorsFile:
        # Prepare output file
        outputCreated = False
        attemptCounter = 0
        outputFileNameFinal = ""
        outputFile = None
        while not outputCreated:
            try:
                # The 'w' means open for exclusive creation, failing if the file already exists.
                outputFileNameFinal = outputFileName + str(attemptCounter) + outputExtension
                outputFile = open(outputFileNameFinal, 'x')
                if outputFile.writable():
                    outputFile.write('"Actor","Title", "Role"\n')
                    outputCreated = True
            except FileExistsError:
                attemptCounter += 1

        # Start reading in the input file
        currentActor = None
        for line in actorsFile:
            lineCounter += 1
            # Useful content starts here.
            if lineCounter > headerOffset:
                lineData = line.strip().split('\t')
                dataLength = len(lineData)

                if dataLength == 1 and len(lineData[0]) == 0:
                    # Reached end of list for an actor.
                    currentActor = None
                else:
                    movieTitle = None
                    role = None

                    if dataLength > 1:
                        # This is an actor line
                        currentActor = lineData[0]
                        if currentActor is None:
                            print("Error: actor was None!")
                            print(lineData)
                            exit()
                        movieTitle = re_movie_title.match(lineData[dataLength - 1])
                        role = re_role.match(lineData[dataLength - 1])
                    elif dataLength == 1:
                        # This is a list of movies for a prev. seen actor
                        if re_eof.match(lineData[0]) is not None:
                            print("Reached end of file.")
                            exit()
                        movieTitle = re_movie_title.match(lineData[0])
                        role = re_role.search(lineData[0])
                    # Check if the movie title was correctly found
                    if movieTitle is not None:
                        movieTitle = movieTitle.group(0)
                        if currentActor is not None:
                            # We have the actor and the movie title.
                            # Now find the role, if it exists.
                            if role is not None:
                                role = role.group(1)
                            else:
                                role = ""
                            output = '"' + str(currentActor) + '","' + str(movieTitle) + '","' + str(role) + '"\n'
                            outputFile.write(output)
                        else:
                            print("Error: Found movie without actor!")
                            print(lineData)
                            exit()
        outputFile.close()
else:
    print("File does not exist: " + actorsFileName)
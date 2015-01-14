__author__ = 'Thom Hurks'

import os

moviesFileName = "movies-converted.list"
outputFileName = "movies"
outputExtension = ".csv"

lineCounter = 0
# Useless IMDb header
headerOffset = 15

if os.path.isfile(moviesFileName):
    with open(moviesFileName) as moviesFile:
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
                    outputFile.write('"Title","Year"\n')
                    outputCreated = True
            except FileExistsError:
                attemptCounter += 1
        # Start reading in the input file
        for line in moviesFile:
            lineCounter += 1
            # Useful content starts here.
            if lineCounter > headerOffset:
                # Lines that start with double quotes are tv-series.
                if str(line[0]) is not "\"":
                    lineData = line.strip().split('\t')
                    # There can be an arbitrary number of tabs between the data.
                    filtered_line = []
                    for entry in lineData:
                        if len(entry) > 0:
                            filtered_line.append(entry)
                    if len(filtered_line) > 1:
                        outputFile.write('\"' + filtered_line[0] + '\",\"' + filtered_line[1] + '\"\n')
                    else:
                        print(str(filtered_line))
        outputFile.close()
else:
    print("File does not exist: " + moviesFileName)
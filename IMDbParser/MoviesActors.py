__author__ = 'Thom Hurks'

import csv
import os
import sys

moviesFileName = "combined_movies.csv"
actorsFileName = "actors.csv"
outputFileName = "movies_actors"
outputExtension = ".csv"
imdbMoviesDict = dict()

if os.path.isfile(moviesFileName):
    duplicatesCounter = 0
    movieCount = 0
    with open(moviesFileName) as moviesFile:
        reader = csv.reader(moviesFile)
        for line in reader:
            movieCount += 1
            imdb_title = line[1]
            movie = imdbMoviesDict.get(imdb_title, None)
            if movie is None:
                movie = imdbMoviesDict[imdb_title] = []
            else:
                duplicatesCounter += 1
            movie.append(line)

    print("Done reading in " + str(movieCount) + " movies. Found " + str(duplicatesCounter) + " duplicate movies.")

    outputCreated = False
    attemptCounter = 0
    outputFileNameFinal = ""
    outputFile = None
    while not outputCreated:
        try:
            # The 'x' means open for exclusive creation, failing if the file already exists.
            outputFileNameFinal = outputFileName + str(attemptCounter) + outputExtension
            outputFile = open(outputFileNameFinal, 'x')
            if outputFile.writable():
                outputFile.write('"imdb_id","imdb_title","Actor", "Role"\n')
                outputCreated = True
        except FileExistsError:
            attemptCounter += 1

    counter = 0
    print("Processing actors file...")
    if os.path.isfile(actorsFileName):
        with open(actorsFileName) as actorsFile:
            reader = csv.reader(actorsFile)
            for line in reader:
                counter += 1
                actor = line[0]
                imdb_title = line[1]
                role = line[2]
                movies = imdbMoviesDict.get(imdb_title, None)
                if movies is not None:
                    for movie in movies:
                        imdb_id = movie[0]
                        outputFile.write('"' + imdb_id + '","' + imdb_title + '","' + actor + '", "' + role + '"\n')
                if counter % 5 == 0:
                    sys.stdout.write("\r Progress: " + str(counter) + " / 3054")
                    sys.stdout.flush()
    else:
        print("Couldn't open actors file! " + actorsFileName)
else:
    print("Couldn't open movies file! " + moviesFileName)
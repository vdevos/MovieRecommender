__author__ = 'Thom Hurks'

import json
import csv
import re
import os
import sys

moviesFileName = "movies.csv"
outputFileName = "combined_movies"
outputExtension = ".csv"
metacriticMoviesFileName = "metacritic_imdb_ids.json"
moviesDictByYear = dict()

failedCounter = 0
successCounter = 0
totalCount = 0

# Titles cannot start with a double quote, else it's a tv episode.
re_movie_title = re.compile("(.+)(?: \((?:\d{4}|\?{4})/?[IXV]*\)|\{.+\})")

# Prepare output file
outputCreated = False
attemptCounter = 0
outputFileNameFinal = ""
outputFile = None
failuresFile = None
while not outputCreated:
    try:
        # The 'w' means open for exclusive creation, failing if the file already exists.
        outputFileNameFinal = outputFileName + str(attemptCounter) + outputExtension
        outputFile = open(outputFileNameFinal, 'x')
        if outputFile.writable():
            outputFile.write('"imdb_id","imdb_title","Title","Year"\n')
            outputCreated = True
            failuresFile = open(outputFileName + str(attemptCounter) + "_failures.txt", 'x')
    except FileExistsError:
        attemptCounter += 1

if os.path.isfile(moviesFileName):
    with open(moviesFileName) as moviesFile:
        reader = csv.reader(moviesFile)
        for line in reader:
            title = line[0]
            normalizedTitle = re_movie_title.match(title)
            if normalizedTitle is not None:
                normalizedTitle = normalizedTitle.group(1)
            else:
                normalizedTitle = title
            year = str(line[1])
            if year.isnumeric():
                year = int(year)
                yearList = moviesDictByYear.get(year, None)
                if yearList is None:
                    yearList = moviesDictByYear[year] = []
                yearList.append([normalizedTitle, title])
        print("Loaded in all IMDb movies.")
if os.path.isfile(metacriticMoviesFileName):
    with open(metacriticMoviesFileName) as metacriticMovies:
        print("Scanning MetaCritic file...")
        for line in metacriticMovies:
            totalCount += 1
            line = json.loads(line)
            imdb_id = line['imdb_id']
            success = False
            if imdb_id is not None and len(imdb_id) > 0:
                year = line['year']
                if year is not None:
                    year = int(year)
                    title = str(line['title'])
                    orgTitle = str(line['orgtitle'])
                    titleFolded = title.casefold()
                    orgTitleFolded = orgTitle.casefold()
                    titleFoldedLength = len(titleFolded)
                    orgTitleFoldedLength = len(orgTitleFolded)
                    yearList = moviesDictByYear.get(year, None)
                    if yearList is not None:
                        smallestDifference = 1000
                        smallestReverseDifference = 1000
                        outputString = ""
                        reverseMatchOutputString = ""
                        for entry in yearList:
                            normalizedTitle = str(entry[0])
                            imdb_title = str(entry[1])
                            entryFolded = str(normalizedTitle).casefold()
                            entryFoldedLength = len(entryFolded)
                            reverseFound = -1
                            difference = 1000
                            reverseDifference = 1000
                            found = entryFolded.find(titleFolded)
                            if found is not -1:
                                # found
                                difference = abs(entryFoldedLength - titleFoldedLength)
                            else:
                                # try again with orgTitle
                                found = entryFolded.find(orgTitleFolded)
                                if found is not -1:
                                    difference = abs(entryFoldedLength - orgTitleFoldedLength)
                                elif entryFoldedLength > 1:  # doing this with single chars is dangerous
                                    # Try the reverse matching with title
                                    reverseFound = titleFolded.find(entryFolded)
                                    if reverseFound is not -1:
                                        reverseDifference = abs(entryFoldedLength - titleFoldedLength)
                                    else:
                                        # Try the reverse matching with orgTitle
                                        reverseFound = orgTitleFolded.find(entryFolded)
                                        if reverseFound is not -1:
                                            reverseDifference = abs(entryFoldedLength - orgTitleFoldedLength)
                            # one of the 4 checks matched
                            if found is not -1:
                                if difference < smallestDifference:
                                    smallestDifference = difference
                                    outputString = '"' + imdb_id + '","' + imdb_title + '","' + title + '","' + str(year) + '"\n'
                                    success = True
                            elif reverseFound is not -1:
                                if reverseDifference < smallestReverseDifference:
                                    smallestReverseDifference = reverseDifference
                                    reverseMatchOutputString = '"' + imdb_id + '","' + imdb_title + '","' + title + '","' + str(year) + '"\n'
                                    success = True
                        if success:
                            if len(outputString) > 0:
                                outputFile.write(outputString)
                                successCounter += 1
                            elif len(reverseMatchOutputString) > 0:
                                outputFile.write(reverseMatchOutputString)
                                successCounter += 1
            if success is False:
                failedCounter += 1
                failuresFile.write(str(line) + "\n")
            if totalCount % 5 == 0:
                sys.stdout.write("\r Progress: " + str(totalCount) + " / 6776")
                sys.stdout.flush()
        print("\nDone!")
        print("Successful matches: " + str(successCounter))
        print("Failures: " + str(failedCounter))








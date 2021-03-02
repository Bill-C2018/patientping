'''
This is the more general version 
it will list each link in the chain
''' 
import sys

class MovieData:
    
    def __init__(self,name,actors):
        self.name = name
        self.actors = actors
        
    


#=======================================
'''
a blank line precedes each movie name
followed by one actor per line.
a blank line ends the current movie and the next line 
starts a new movie
'''
def ReadMovieData(fileName):
    
    movieDict = dict()
    movies = MovieData("",[])
    
    with open(fileName) as filein:
        while True:
            line = filein.readline()

            if not line:
                break

            if line == "\r" or line == "\n" or line == "\r\n" or line == "" or line == " ":
                if movies.name != "":
                    movieDict[movies.name] = movies.actors
                #next line is movie name
                line = filein.readline()
                if not line:
                    break
                line = line.replace("\r","")
                line = line.replace("\n","")
                movies.actors = []
                movies.name = line
                continue
            
            line = line.replace("\r","")
            line = line.replace("\n","")
            movies.actors.append(line)
            
    #grab the last set of actors for the last movie            
    movieDict[movies.name] = movies.actors        
    return movieDict            
            

#return a list of movies that the actor was in 
def GetMoviesWithActor(actor,mydict):
    
    movies = []
    for k in mydict.keys():
        if actor in mydict[k]:
            movies.append(k)
    
    return movies

#returns a set of all the actors that were in a list of movies
def SetOfCommonActors(listofmovies,mydict):
    
    commonActors = set()
    
    for k in range(len(listofmovies)):
        tempset = set(mydict[listofmovies[k]])
        commonActors |= tempset
        
    return commonActors

#so we dont mess up the order of the lists themselves
#do this in a seperate function
def compareListOfMovies(list1,list2): 
    return set(list1) & set(list2)    
 
def BuildSeperationChain(setOfActorsA,mydict,listOfMoviesB,listOfMoviesA):

    seen = []
    name = ""
    res = set()    
    while setOfActorsA:
        name = setOfActorsA.pop(0)
        while name in seen:
            if setOfActorsA:
                name = setOfActorsA.pop(0)
            else:
                break

        seen.append(name)
        la = GetMoviesWithActor(name,mydict)
        setOfActorsA = setOfActorsA + list(SetOfCommonActors(la, mydict))
        res = compareListOfMovies(la,listOfMoviesB)
        if len(res) > 0:
            break 
            
    return (name,res)

def DoTheWork(name1,name2,mydict):
    
    depth = 1
    text = ""
    listOfMoviesA = GetMoviesWithActor(name1,mydict)
    listOfMoviesB = GetMoviesWithActor(name2,mydict)
    res = compareListOfMovies(listOfMoviesA,listOfMoviesB)
    '''
    if both were in the same movie we can end it here
    '''
    if res:
        return (f"{name1} was in {res.pop()} with {name2} ",depth)
        
    else:

        setOfActorsA = SetOfCommonActors(listOfMoviesA, mydict)
        setOfActorsB = SetOfCommonActors(listOfMoviesB, mydict)
        restuple = BuildSeperationChain(list(setOfActorsA),mydict,listOfMoviesB,listOfMoviesA)
#=============================================
#
#   we now have the "deepest" link in the chain . walk it back 
#   up to build the output
#
#=============================================
        if restuple[1]:
            text = text + f"{restuple[0]} was in {restuple[1].pop()} with {name2}" 
        while True:
            depth += 1
            name2 = restuple[0]
            listOfMoviesA = GetMoviesWithActor(name1,mydict)
            listOfMoviesB = GetMoviesWithActor(name2,mydict)
            res = compareListOfMovies(listOfMoviesA,listOfMoviesB)
            if res:
                text = text + f" who was in {res.pop()} with {name1} "
                return (text, depth)
            else:
                setOfActorsA = SetOfCommonActors(listOfMoviesA, mydict)
                setOfActorsB = SetOfCommonActors(listOfMoviesB, mydict)
                restuple = BuildSeperationChain(list(setOfActorsA),mydict,listOfMoviesB,listOfMoviesA)
                if restuple[1]:
                    text = text + f" who was in {restuple[1].pop()} with {restuple[0]} "
                else:
                    return ("None found",0)
    return ("None found",0)
 
def GetStringDegreesBetween(name1, name2,mydict):
    
    res = DoTheWork(name1,name2,mydict)
    return res[0]
  
def GetDegreesBetween(name1, name2,mydict):
    res = DoTheWork(name1,name2,mydict)
    return res[1]
     
#=======================================
if __name__ == "__main__":

    
#    name1 =""
#    name1 = "Pierce Brosnan"
#    name2 = "Tilda Swinton"
 #   name2 = "Meryl Streep"
#    name2 = "Henry Czerny"
#    name2 = "bill bobbit"
#   name2 = "Vanessa Redgrave"
#    name2 = "joe shmoe"
#    name2 = ""
#    name2 = "Jean Reno"
#    name2 = "Sean Bean"
#    name2 = "Izabella Scorupco"

    if len(sys.argv) < 3:
        print ("Invalid args")
        exit(1)
        
    name1 = sys.argv[1]
    name2 = sys.argv[2]
    

    
    mydict = ReadMovieData("data.txt")
    depth = 1
    
    
    res = GetStringDegreesBetween(name1, name2,mydict)
    print (res)
    
    res = GetDegreesBetween(name1, name2,mydict)
    print (res)
  
    
    
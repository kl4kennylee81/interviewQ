
# dictionary mapping position -> asteroid
def isHit(posToAsteroid,pos,t):
    # hit eschaton
    if pos < 0:
        return True
    elif pos not in posToAsteroid:
        return False
    else:
        start,cycle_time = posToAsteroid[pos]
        asteroid_offset = (start+t) % cycle_time
        return asteroid_offset == 0

def createRoutePermutationRec(totalTime,permutations,setAvailable,curRoute):
    if totalTime == 0:
        permutations.append(curRoute)
    else:
        for accel in setAvailable:
            createRoutePermutationRec(totalTime-1,permutations,setAvailable,curRoute+[accel])


def createRoutePermutation(totalTime,setAvailable):
    permutations = []
    createRoutePermutationRec(totalTime,permutations,setAvailable,[])
    return permutations;

def simulateRoute(route,escapePos,posToAsteroid,maxTime):

    curPos = 0
    curV = 0

    for t in range(maxTime):
        # escaped in t
        if isHit(posToAsteroid,curPos,t):
            return -1
        else:
            if t < len(route):
                accel = route[t]
            else:
                accel = 0

            curV+=accel
            curPos+=curV
            if curPos > escapePos:
                return t+1
    return -1

# for a particular position an asteroid can have 2 <= cycle < totalTime
# with 0 <= offset < cycle
def generatePermuteAsteroids(totalTime,totalPos):
    asteroid_li = []
    generatePermuteAsteroidsRec(totalTime,totalPos,asteroid_li,[])
    return asteroid_li


def generatePermuteAsteroidsRec(totalTime,totalPos,asteroid_li,curAsteroids):
    if totalPos == 0:
        asteroid_li.append(curAsteroids)
    else:
        for cycle in xrange(2,totalTime):
            for start in xrange(cycle):
                asteroid = (start,cycle)
                generatePermuteAsteroidsRec(totalTime,totalPos-1,asteroid_li,curAsteroids+[asteroid])

def convertAsteroidListToDict(asteroids):
    posToAsteroid = dict()
    pos = 0
    for asteroid in asteroids:
        pos+=1
        posToAsteroid[pos] = asteroid
    return posToAsteroid

def simulateAllRoute(t,escapePos,posToAsteroid):
    allRoutes = createRoutePermutation(t,[-1,0,1])
    timeCompleteToRoutes = dict()
    for route in allRoutes:
        completeTime = simulateRoute(route,escapePos,posToAsteroid,t)
        if completeTime != -1:
            timeCompleteToRoutes.setdefault(completeTime,[]).append(route)

    # find the shortest t
    min_t = None
    for completeTime,routes in timeCompleteToRoutes.iteritems():
        if min_t == None:
            min_t = completeTime
        else:
            if completeTime < min_t:
                min_t = completeTime
    if min_t == None:
        return (-1,[])
    else:
        # collected all routes that completed the fastest
        segment_routes = []
        for route in timeCompleteToRoutes[min_t]:
            segment_route = route[:min_t]
            if not segment_route in segment_routes:
                segment_routes.append(segment_route)

        return (min_t,segment_routes)

def simulateAllRouteAllAsteroid(t,escapePos):
    # create all possible asteroids
    asteroid_li = generatePermuteAsteroids(t,escapePos)
    asteroidToRoutes = dict()

    for asteroids in asteroid_li:
        posToAsteroid = convertAsteroidListToDict(asteroids)
        min_t,routes = simulateAllRoute(t,escapePos,posToAsteroid)
        str_asteroids = str(asteroids)
        asteroidToRoutes[str_asteroids] = (min_t,routes)

    return asteroidToRoutes

def dynamicRouteFinder(t,escapePos,posToAsteroid):
    rows = escapePos*2
    col = t
    [[-1 for i in range(col)] for j in range(rows)]


def main():

    # asteroids are (start,cycle_time)
    # with an asteroid position equal to (start+t) % cycle_time

    asteroidToRoutes = simulateAllRouteAllAsteroid(4,4)
    counter = 0
    for asteroids,(min_t,routes) in asteroidToRoutes.iteritems():
        counter+=1
        print("{}.Asteroid:".format(counter))
        print(asteroids)
        print("time:{}".format(min_t))
        print("Route:{}\n".format(routes))

    # asteroid_li = [(0,2),(1,3),(3,4),(1,2)]
    # posToAsteroid = convertAsteroidListToDict(asteroid_li)
    # time = simulateRoute([-1],4,posToAsteroid,10)
    # print(time)




if __name__ == "__main__":
    main()
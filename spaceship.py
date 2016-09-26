from __future__ import print_function
import json
import numpy
import sys
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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

def simulateRoute(route,escapePos,posToAsteroid,blast_time):

    curPos = 0
    curV = 0

    maxTime = blast_time * escapePos
    blast_pos = -1
    for t in range(min(len(route),maxTime)):
        if t % blast_time == 0:
            blast_pos += 1

        if curPos < blast_pos:
            return -1

        # escaped in t
        if isHit(posToAsteroid,curPos,t,blast_pos):
            return -1
        else:
            if t < len(route):
                accel = route[t]

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

def simulateAllRouteAllAsteroid(blast_t,escapePos):
    # create all possible asteroids
    asteroid_li = generatePermuteAsteroids(blast_t,escapePos)
    asteroidToRoutes = dict()

    for asteroids in asteroid_li:
        min_t,routes = simulateAllRoute(blast_t,escapePos,asteroids)
        str_asteroids = str(asteroids)
        asteroidToRoutes[str_asteroids] = (min_t,routes)

    return asteroidToRoutes

# array mapping position index -> asteroid
def isHit(posToAsteroid,pos,t,blast_pos):
    # hit eschaton
    if pos < 0:
        return True
    elif pos < blast_pos:
        return True
    elif pos == 0:
        return False
    elif pos >= len(posToAsteroid):
        return False
    else:
        start,cycle_time = posToAsteroid[pos-1]
        asteroid_offset = (start+t) % cycle_time
        return asteroid_offset == 0

def getPrev(matrix,cur_v,time,prev_p):
    if prev_p < 0 or prev_p >= len(matrix[0]):
        return None

    if cur_v+1 < len(matrix) and matrix[cur_v+1][prev_p][time-1] != None:
        route = matrix[cur_v+1][prev_p][time-1]
        return route + [-1]
    if cur_v-1 > 0 and matrix[cur_v-1][prev_p][time-1] != None:
        route = matrix[cur_v-1][prev_p][time-1]
        return route + [1]

    if matrix[cur_v][prev_p][time-1] != None:
        route = matrix[cur_v][prev_p][time-1]
        return route +[0]
    
    return None

def printMatrix(matrix):
    for row in matrix:
        eprint("{}\n".format(row))

# def dynamicRouteFinder(t,escapePos,posToAsteroid):
#     velocity_bound = escapePos*2
#     time_bound = t+1
#     pos_bound = escapePos*2
#     # rows is the possible velocity
#     # columns are the time t
#     # values are the position
#     eprint("starting matrix creation")
#     matrix = [[[None for k in xrange(time_bound)] for i in xrange(pos_bound)] for j in xrange(velocity_bound)]

#     eprint("finished matrix creation")
#     start_v_index = escapePos
#     matrix[start_v_index][0][0] = []
#     count = 0
#     for time in range(1,len(matrix[0][0])):
#         for velocity in range(len(matrix)):
#             for position in range(len(matrix[0])):
#                 count+=1
#                 actual_v = velocity - escapePos
#                 prev_pos = position - actual_v

#                 # time t-1 has velocity v+1, and accelerated -1 accel
#                 # to get to current velocity

#                 if isHit(posToAsteroid,position,time):
#                     continue

#                 cur_route = getPrev(matrix,velocity,time,prev_pos)

#                 if position > escapePos and cur_route != None:
#                     return time,cur_route
#                 matrix[velocity][position][time] = cur_route
#                 # eprint("count:{}:time:{}".format(count,time))
#                 eprint("count:{}:time:{}:v:{}:p:{}".format(count,time,actual_v,position))
#     return None

def nextLayer(entry,blast_pos):
    (p,v),course = entry
    nextLayer = []

    accels = [-1,0,1]
    for accel in accels:
        up_v = v+accel
        up_p = p+up_v
        up_course = course + [accel]
        if up_p >= blast_pos:
            nextLayer.append((up_p,up_v,up_course))
    return nextLayer



def dynamicRouteFinder(blast_t,escapePos,asteroid_li):
    velocity_bound = escapePos*2
    time_bound = blast_t * escapePos
    pos_bound = escapePos*2
    # rows is the possible velocity
    # columns are the time t
    # values are the position
    prev_frontier = dict()
    initial_state = (0,0)
    prev_frontier[initial_state] = []
    t = 1
    blast_pos = 0
    while t <= time_bound:
        cur_frontier = dict()
        allLayer = []
        for entry in prev_frontier.iteritems():
            (p,v),course = entry
            nextLay = nextLayer(entry,blast_pos)
            allLayer+=nextLay
            for new_p,new_v,new_course in nextLay:
                if new_p > escapePos:
                    return (t,new_course)

                if isHit(asteroid_li,new_p,t,blast_pos):
                    continue
                cur_frontier[(new_p,new_v)] = new_course

        if len(cur_frontier) == 0:
            return None
        prev_frontier = cur_frontier
        if t % blast_t == 0:
            blast_pos += 1
        
        t+=1

    return None

def simulateAllRouteAllAsteroid(blast_t,escapePos):
    # create all possible asteroids
    asteroid_li = generatePermuteAsteroids(blast_t,escapePos)
    asteroidToRoutes = dict()

    for asteroids in asteroid_li:
        min_t,routes = simulateAllRoute(blast_t,escapePos,asteroids)
        str_asteroids = str(asteroids)
        asteroidToRoutes[str_asteroids] = (min_t,routes)

    return asteroidToRoutes

def compareResults(blast_t,escapePos):
    asteroid_li = generatePermuteAsteroids(blast_t,escapePos)

    for asteroids in asteroid_li:
        result = dynamicRouteFinder(blast_t,escapePos,asteroids)
        if result != None:
            min_t,route = result
            compareResult(blast_t,escapePos,asteroids,min_t,route)


def compareResult(blast_time,escapePos,posToAsteroid,min_t,route):

    simulate_t = simulateRoute(route,escapePos,posToAsteroid,blast_time)

    assert(simulate_t != -1)
    assert(simulate_t == min_t)

def getAsteroidsFromJson(asteroids_json):

    json_li = numpy.array(asteroids_json)
    asteroids_li = []
    count = 0
    for asteroid_str in json_li:
        offset = int(asteroid_str["offset"])
        t_cycle = int(asteroid_str["t_per_asteroid_cycle"])
        asteroids_li.append((offset,t_cycle))
    return asteroids_li

def runSimulator(json):
    t,escapePos,posToAsteroid = parseChartJson(json)
    result = dynamicRouteFinder(t,escapePos,posToAsteroid)
    return result

def parseChartJson(json):
    asteroid_li = getAsteroidsFromJson(json["asteroids"])
    # posToAsteroid = convertAsteroidListToDict(asteroid_li)
    escapePos = len(asteroid_li)
    blast_t = int(json["t_per_blast_move"])
    return (blast_t,escapePos,asteroid_li)

def runComparator(json):
    t,escapePos,posToAsteroid = parseChartJson(json)
    min_t,min_route = dynamicRouteFinder(t,escapePos,posToAsteroid)
    compareResult(t,escapePos,posToAsteroid,min_t,min_route)

    return min_t,min_route

def main():
    fname = "sampleChart.json"
    output_name = "output.json"
    if len(sys.argv[1:]) > 0:
        fname = sys.argv[1]
        if len(sys.argv[2:]) > 0:
            output_name = ssys.argv[2]
    json_data = None
    with open(fname) as json_file:
        json_str = json_file.read()
        json_data = json.loads(json_str)

    result = runComparator(json_data)
    if result != None:
        min_t,min_route = result

        route_json = json.dumps(min_route)

        with open(output_name,'w') as output:
            output.write(route_json)
    else:
        print("no solution")






if __name__ == "__main__":
    main()
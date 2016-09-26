import json
import numpy
import sys

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

# posToAsteroid: array mapping position index -> asteroid
def isHit(posToAsteroid,pos,t,blast_pos):
    # hit eschaton
    if pos < 0:
        return True
    # hit by blast
    elif pos < blast_pos:
        return True
    # initial position safe checked after blast
    elif pos == 0:
        return False
    # past asteroid belt
    elif pos >= len(posToAsteroid):
        return False
    else:
        start,cycle_time = posToAsteroid[pos-1]
        asteroid_offset = (start+t) % cycle_time
        return asteroid_offset == 0

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

if __name__ == "__main__":
    main()
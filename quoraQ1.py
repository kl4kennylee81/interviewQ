import collections

def sign(x): return (x > 0) - (x < 0)

  # get leftmost contiguous streak of numbers
  # positive being a streak of increasing numbers
  # negative being a streak of decreasing numbers
  # 0 being the number stayed unchanged
def numInARow(compareTo,start,end):
  if (len(compareTo) > 0):
    streak = compareTo[start]
    i = start + 1
    while(i < end):
      if (sign(streak) == 0):
        break
      
      if sign(streak) == sign(compareTo[i]):
        streak += compareTo[i]
        i+=1
      else:
        break

    return streak
  else:
    return 0

def getInARowList(compareTo,start,end):
  i = start
  inARow_li = collections.deque()
  while(i < end):
    streak = numInARow(compareTo,i,end)
    if (streak != 0):
      inARow_li.append(streak)
      i+=abs(streak)
    else:
      inARow_li.append(0)
      i+=1
  return inARow_li

def getNumSubRanges(compareTo,start,end):

  inARowList = getInARowList(compareTo,start,end)
  numSubRanges = 0
  for entry in inARowList:
    numSubRanges += signedSumtoN(entry + sign(entry))

  return numSubRanges

def signedSumtoN(entry):
  return sign(entry)*(entry * (entry-sign(entry)))/2


  # comparing i and i+1
  # 1 being if i+1 is greater to i (increasing)
  # 0 being if i+1 is equal to i (stays the same)
  # -1 being if i+1 is less than i (decreasing)
def createCompareTo(li,n,k):
  compareTo = collections.deque()
  for i in range(n-1):
    if (li[i] == li[i+1]):
      compareTo.append(0)
    elif (li[i] < li[i+1]):
      compareTo.append(1)
    elif (li[i] > li[i+1]):
      compareTo.append(-1)
  
  return compareTo


def upVote(li,n,k):
  compareTo = createCompareTo(li,n,k)

  inARowList = getInARowList(compareTo,0,k-1)

  curSubRanges = getNumSubRanges(compareTo,0,k-1)

  windows = [curSubRanges]
  numWindows = n-k+1
  print("compareTo: "+str(compareTo))
  for i in range(1,numWindows):
    curNewEntry = compareTo[k+i-2]
    curDeletedEntry = compareTo[i-1]

    print("cur new i: "+str(curNewEntry))
    print("iteration i: "+str(inARowList))
    if len(inARowList) > 0:
      if sign(curNewEntry) == 0:
        inARowList.append(0)
      elif sign(inARowList[len(inARowList)-1]) == sign(curNewEntry):
        inARowList[len(inARowList)-1]+=curNewEntry
        curSubRanges += inARowList[len(inARowList)-1]
      else:
        inARowList.append(curNewEntry)
        curSubRanges += curNewEntry

      print(curSubRanges)


      if sign(curDeletedEntry) == 0:
        inARowList.popleft()
      elif sign(inARowList[0]) == sign(curDeletedEntry):        
        diff = inARowList[0] - sign(curDeletedEntry)
        if diff == 0:
          inARowList.popleft()
          curSubRanges-= curDeletedEntry
        else:
          curSubRanges -= inARowList[0]
          inARowList[0] = diff

      print(curSubRanges)

      windows.append(curSubRanges)

  print("iteration final: "+str(inARowList))
  return windows











def main():
  li = [1,2,4,5,6,4,3,2,1,2]
  print("initial: "+str(li))
  result = upVote(li,len(li),4);
  print("result: " + str(result))

  # li = [-1,1,0,1,1]
  # print(getNumSubRanges(li,0,len(li)))

if __name__ == "__main__":
  main()

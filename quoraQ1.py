import collections
import sys
import fileinput
# import timing

'''
Quora Challenge 1: Upvotes
This solution involves finding the number of subranges of the initial windows
then using that value and the diff on the left and right end as we slide the windows
to find the value of the new window. We keep track of the number of contiguous streaks
of +/- in a deque so we can update on both the left and the right end as we slide the window

1. 1st step was creating a new list with entry of 1/0/-1 i and i+1 is increasing/the same/decreasing

2. using this compareTo list we then create the initial windows deque
of a list of the number of contiguous intervals of nonDecreasing numbers.
With any value > 0 being an interval of nonDecreasing numbers and a 0 being a 
placeholder for a decreasing interval. 
Using this and the formula subranges = n(n-1)/2. we can calculate the first windows
number of nonDecreasing subranges

3. Then we iterate through from 1 ->n-k+1 windows(since we have the initial window) 
and then using the initial window value we update to the right end of the deque to
add the new value in the window and update the left end of the deque to delete the old
value no longer in the window. We can then calculate in O(1) time using the previous window
value and changing the left and right ends the new windows number of subranges.

4. Then we create a list of numbers of contiguous intervals of nonIncreasing numbers.
We will use this to update the values by subtracting the number of nonIncreasing subRanges.

5. We follow the same process as step (3) and we subtract the number of
nonIncreasing subranges from the windows from 1 -> n-k+1.

6. We then return the windows

The runtime of this function is O(n) since we are only processing each element once in one pass 
as we slide the window we utilize the existing number of subranges from the last window to calculate the
number of subranges in the new window by diffing from the right and left end in O(1) time each. And since
we do one pass for the nonDecreasing and another pass for the nonIncreasing that is two passes each of
which's runtime is O(n) which is still O(n).
'''

def solution():
  line1 = str(raw_input()).split(" ")
  n = int(line1[0])

  k = int(line1[1])

  num_list = []
  for line in fileinput.input():
    num_list+=line.strip().split(" ")

  num_list = map(long, num_list)
  # num_list = num_list[:2235]

  # n = 2234

  window_sr_li = upVote(num_list,n,k)

  for entry in window_sr_li:
    print(entry)
  return window_sr_li

  for entry in num_list:
    continue
  
def sign(x): return (x > 0) - (x < 0)

def numZerosInARow(compareTo,start,end):
  numZeros = 0
  for i in range(start,end):
    if (compareTo[i] == 0):
      numZeros += 1
    else:
      break
  return numZeros

  # get leftmost contiguous streak of numbers
  # positive being a streak of nondecreasing numbers
  # negative being a streak of nonincreasing numbers
def numInARow(compareTo,start,end,nonDecreasing):
  if (len(compareTo) > 0):
    # find number of zeros in a row
    numZeros_InARow = numZerosInARow(compareTo,start,end)
    first_nonZero_i = start+numZeros_InARow

    if (first_nonZero_i < end):
      if ((nonDecreasing and compareTo[first_nonZero_i] != -1) or
          (not nonDecreasing and compareTo[first_nonZero_i] != 1)):
        streak = compareTo[first_nonZero_i] + sign(compareTo[first_nonZero_i])*numZeros_InARow
        i = first_nonZero_i + 1
        while(i < end):
          if (sign(compareTo[i]) == 0):
            streak += sign(streak)
            i+=1
          
          elif sign(streak) == sign(compareTo[i]):
            streak += compareTo[i]
            i+=1
          else:
            break

        return streak
      else:
        if nonDecreasing:
          return numZeros_InARow;
        else:
          return -numZeros_InARow;
    else:
        if nonDecreasing:
          return numZeros_InARow;
        else:
          return -numZeros_InARow;


  else:
    return 0
  # for i in range(start,end):
  #   x = 1

def getInARowList(compareTo,start,end,nonDecreasing):
  i = start
  inARow_li = collections.deque()
  while(i < end):
    streak = numInARow(compareTo,i,end,nonDecreasing)
    if (streak != 0):
      inARow_li.append(streak)
      i+=abs(streak)
    else:
      inARow_li.append(0)
      i+=1
  return inARow_li

def getNumSubRanges(inARowList):

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

def updateSubRangeWindows(compareTo,inARowList,curSubRange,windows,k,nonDecreasing):

  numWindows = len(windows)
  curSubRanges = curSubRange
  for i in range(1,numWindows):
    curNewEntry = compareTo[k+i-2]
    curDeletedEntry = compareTo[i-1]

    if len(inARowList) > 0:
      if (sign(curNewEntry) == -1 and nonDecreasing or
          sign(curNewEntry) == 1 and not nonDecreasing):
        inARowList.append(0)

      elif sign(curNewEntry) == 0:
        if inARowList[len(inARowList)-1] == 0:
          if nonDecreasing:
            inARowList.append(1)
            curSubRanges += inARowList[len(inARowList)-1]
          else:
            inARowList.append(-1)
            curSubRanges += inARowList[len(inARowList)-1]
        else:
          inARowList[len(inARowList)-1]+=sign(inARowList[len(inARowList)-1])
          curSubRanges += inARowList[len(inARowList)-1]

      elif sign(inARowList[len(inARowList)-1]) == sign(curNewEntry):
        inARowList[len(inARowList)-1]+=curNewEntry
        curSubRanges += inARowList[len(inARowList)-1]
      else:
        inARowList.append(curNewEntry)
        curSubRanges += curNewEntry

      if (sign(curDeletedEntry) == -1 and nonDecreasing or
          sign(curDeletedEntry) == 1 and not nonDecreasing):
          inARowList.popleft()


      elif (sign(curDeletedEntry) == 0 or
            sign(inARowList[0]) == sign(curDeletedEntry)):        
        diff = inARowList[0] - sign(inARowList[0])
        val = sign(inARowList[0])
        if diff == 0:
          inARowList.popleft()
          curSubRanges-= val
        else:
          curSubRanges -= inARowList[0]
          inARowList[0] = diff

      windows[i]+=curSubRanges

  return windows


def upVote(li,n,k):
  
  if len(li) == 0 or n == 0:
    return []

  compareTo = createCompareTo(li,n,k)

  numWindows = n-k+1
  windows = [0 for i in range(numWindows)]

  inARowListPlus = getInARowList(compareTo,0,k-1,True)
  curSubRangesPlus = getNumSubRanges(inARowListPlus)

  windows[0]+=curSubRangesPlus
  windows = updateSubRangeWindows(compareTo,inARowListPlus,curSubRangesPlus,windows,k,True)

  inARowListMinus = getInARowList(compareTo,0,k-1,False)
  curSubRangesMinus = getNumSubRanges(inARowListMinus)

  windows[0]+=curSubRangesMinus
  windows = updateSubRangeWindows(compareTo,inARowListMinus,curSubRangesMinus,windows,k,False)

  return windows

def main():
  # 5 3
  # 1 2 3 1 1

  solution()

  # li = [1,2,3,1,1]

if __name__ == "__main__":
  main()

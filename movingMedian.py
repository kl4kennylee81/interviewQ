from collections import deque
import sys

class Average:

  def __init__(self,k):
    self.k = k
    self.window = deque()
    self.cur_avg = 0

  def processElement(self,new_val):
    avg = self.movingAvg(new_val)
    if avg != -1:
      print(avg)

  def movingAvg(self,new_val):
    self.window.append(new_val)
    # will only get called to create first kth window
    if len(self.window) == self.k:
      self.cur_avg = reduce((lambda x,y:x+y),self.window)/float(len(self.window))
      return self.cur_avg

    # with k+1 elements it will pop back to k and calculate
    # the new moving average
    elif len(self.window) > self.k:

      # add on new val running avg
      popped_val = self.window.popleft()

      # length of the window will be k again
      assert(len(self.window) == self.k)

      print(self.window)

      self.cur_avg = self.cur_avg + (float(new_val)/self.k) - (float(popped_val)/self.k)
      return self.cur_avg

    else:
      return -1


class Median:

  def __init__(self,k):
    self.k = k
    self.window = deque()
    self.cur_avg = 0

  def processElement(self,new_val):
    median = self.movingMedian(new_val)
    if median != -1:
      print("MEDIAN:"+str(median))

  def getMedian(self):
    sorted_window = sorted(self.window)
    center = self.k/2
    # even take average of two middle numbers
    if self.k % 2 == 0:
      median = float(sorted_window[center] + sorted_window[center-1])/2
      return median
    # odd take the middle number
    else:
      return sorted_window[center]

  def movingMedian(self,new_val):
    self.window.append(new_val)
    if len(self.window) > self.k:
      self.window.popleft()

    if len(self.window) == self.k:
      return self.getMedian()
    else:
      return -1






def main():
  # window_size = input()
  # avgSolution = Average(window_size)
  # # for new_val in sys.stdin:
  # while(True):
  #   new_val = input()
  #   avgSolution.processElement(new_val)
  window_size = input()
  medianSolution = Median(window_size)
  while(True):
    new_val = input()
    medianSolution.processElement(new_val)

if __name__ == "__main__":
    main()
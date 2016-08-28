"""Module docstring.

This serves as a long usage message.
"""
import sys
import getopt
from collections import deque
import math
import timing

def coinCount(coin_list,amount):
    # base case
    # if list empty
    if (amount == 0):
        return 1;

    if (amount < 0):
        return 0;

    if (len(coin_list) == 0):
        return 0;

    count = 0;
    for i in range(len(coin_list)):
        amount_left = amount;
        while (amount_left > 0):
            amount_left-=coin_list[i];
            count += coinCount(coin_list[i+1:],amount_left);
    return count;


def permutationString(string_list,cur_string):
    if (len(string_list) == 0):
        print(cur_string);
        return;

    for i in range(len(string_list)):
        permutationString(string_list[:i]+string_list[i+1:],cur_string+string_list[i]);

# print ever permutation of n bytes
def permuteBits(n_bits,cur_bits):
    if (n_bits <= 0):
        print(cur_bits);
        return;

    permuteBits(n_bits-1,cur_bits+"0");
    permuteBits(n_bits-1,cur_bits+"1");


# def permuteBitsTable(n_bits,cur_bits):

# you have n letters and print all k < n combinations
# ex. 8 letters and print every 3 letter combination
# no repeats

def combNofK(char_list,k,cur_string):

    if (k == 0):
        print(cur_string);
        return;

    for i in range(len(char_list)):
        combNofK(char_list[:i]+char_list[i+1:],k-1,cur_string+char_list[i]);


# returns the longest chain for the index
def dfs_rec(index,word_graph,wordToLongestChain,visited):
    # this is the memoization
    if (index in visited):
        return wordToLongestChain[index];

    maxdepth = 0;
    for i in range(len(word_graph[index])):
        # have to make sure there exists an edge
        if (not word_graph[index][i]):
            continue;

        depth = 1 + dfs_rec(i,word_graph,wordToLongestChain,visited);
        maxdepth = max(depth,maxdepth);
    
    if (index in wordToLongestChain and index in visited):
        wordToLongestChain[index] = max(maxdepth,wordToLongestChain[index]);
    else:
        visited.add(i);
        wordToLongestChain[index] = maxdepth;

    return maxdepth;


def longestDictionaryChain(word_list):

    word_graph = createWordGraph(word_list);

    wordToLongestChain = dict();

    visited = set();

    for i in range(len(word_list)):
        word = word_list[i];
        longestChain = dfs_rec(i,word_graph,wordToLongestChain,visited);
        wordToLongestChain[i] = longestChain;

    maxLen = 0;
    maxIndex = 0;

    for k,v in wordToLongestChain.iteritems():
        if (v > maxLen):
            maxLen = v;
            maxIndex = k;

    return maxLen;

def createWordGraph(word_list):
    word_graph = [[0 for i in xrange(len(word_list))] for i in xrange(len(word_list))];

    for i in range(len(word_list)):
        for j in range(len(word_list)):
            word_graph[i][j] = isOneDelete(word_list[i],word_list[j]);


    return word_graph;


# returns true if deleting one char in word turns it into word2
# we don't want it to be reflexive since its going to be a DAG
def isOneDelete(word1,word2):
    # only true if it is 1 letter greater in size
    if ((len(word1) - len(word2)) != 1):
        return False;
    else:
        i = 0;
        j = 0;
        edits = 0;
        while (i < len(word1) and j < len(word2)):
            if (edits > 1):
                return False;

            if (word1[i] != word2[j]):
                # print("{} {}\n".format(word1[i],word2[j]));
                i+=1;
                edits+=1;
            else:
                i+=1;
                j+=1;

        return True;

def getFriendGroupSizeBFT(friend_index,friend_graph,visitedBy,groupToSize):
    if (friend_index in visitedBy):
        return groupToSize[visitedBy[friend_index]];
    
    bft_queue = deque();
    bft_queue.append(friend_index);

    size_group = 0;
    while (bft_queue):
        next_index = bft_queue.popleft();
        if (next_index in visitedBy):
            continue;
        else:
            visitedBy[next_index] = friend_index;
            size_group += 1;
            row = friend_graph[next_index];
            for i in range(len(row)):
                # if there is an edge
                if (row[i] == 0):
                    continue;
                # if its been visited before
                if (i in visitedBy):
                    continue;

                else:
                    bft_queue.append(i);

    return size_group;

def getBiggestFriendGroups(friendList):
    friend_graph = friendListsToGraph(friendList);
    return getBiggestFriendGroup(friend_graph);

def getBiggestFriendGroup(friend_graph):
    # represent the group as one person and his connected component
    groupToSize = dict();
    visitedBy= dict();
    for i in range(len(friend_graph)):
        size = getFriendGroupSizeBFT(i,friend_graph,visitedBy,groupToSize);
        groupToSize[i] = size;

    friendGroups = dict();
    for friend,groupLeader in visitedBy.iteritems():
        if (groupLeader in friendGroups):
            friendGroups[groupLeader].append(friend);
        else:
            friendGroups[groupLeader] = [friend];

    max_size = 0;
    max_fl = [];
    for groupLeader,friends in friendGroups.iteritems():
        if (len(friends) > max_size):
            max_size = len(friends);
            max_fl = friends;

    return max_fl;



def friendListsToGraph(friendMap):
    graph = [[0 for i in range(len(friendMap))] for i in range(len(friendMap))];
    nameToIndex = dict();

    cur_i = 0;
    for name,flist in friendMap.iteritems():
        nameToIndex[name] = cur_i;
        cur_i+=1;
    
    cur_i= 0;
    for name,flist in friendMap.iteritems():
        for friend in flist:
            friend_index = nameToIndex[friend];
            graph[cur_i][friend_index] = 1;
        cur_i+=1;

    return graph;

def connectedFriend(friendMap):
    friend_graph = friendListsToGraph(friendMap);
    return connectedFriends(friend_graph);


def connectedFriends(friend_graph):

    # represent the group as one person and his connected component
    groupToSize = dict();
    visitedBy= dict();
    for i in range(len(friend_graph)):
        size = getFriendGroupSizeBFT(i,friend_graph,visitedBy,groupToSize);
        groupToSize[i] = size;

    max_fg_size = 0;
    for friend,size in groupToSize.iteritems():
        if size > max_fg_size:
            max_fg_size = size;

    return max_fg_size;


def mergeStep(li_1,li_2):

    l1_i = 0;
    l2_i = 0;

    new_list = [];

    while (l1_i < len(li_1) or l2_i < len(li_2)):
        if (l2_i == len(li_2)):
            new_list.append(li_1[l1_i]);
            l1_i+=1;
        elif (l1_i == len(li_1)):
            new_list.append(li_2[l2_i]);
            l2_i+=1;          
        elif (li_1[l1_i] > li_2[l2_i]):
            new_list.append(li_2[l2_i]);
            l2_i+=1;
        else:
            new_list.append(li_1[l1_i]);
            l1_i+=1;

    return new_list;



def mergeStepInPlace(li,l1_s,l2_s,l2_e):

    # the sorted position everything to the left of cur_index is sorted
    # and the right of l1_s.
    cur_index = l1_s;

    l2_cur_index = l2_s;

    l1_swapped_length = 0;
    l1_cur_swapped_index = 0;

    num_l1 = l2_s - l1_s;
    num_l2 = l2_e - l2_s;

    while(cur_index != l2_e):
        if (num_l1 == 0):
            break;

        if (cur_index == l2_s):
            break;

        if (l1_swapped_length > 0):
            
            l1_actual_index = l2_s + l1_cur_swapped_index;
        else:
            l1_actual_index = cur_index;

        l1_val = li[l1_actual_index];
        l2_val = li[l2_cur_index];

        if (l1_val > l2_val):
            # print("\n\ncur index:{},val:{} \nl2 index:{},val:{}\n\n".format(cur_index,li[cur_index],l2_cur_index,li[l2_cur_index]));


            # must do the swap so you can have a ring buffer style get
            tempVal = li[cur_index];
            li[cur_index] = li[l2_cur_index];
            li[l2_cur_index] = tempVal;
            
            if (l2_cur_index < l2_e):
                l2_cur_index+=1;

            # setup swapped length
            if (cur_index < l2_s):
                l1_swapped_length+=1;

            num_l2-=1;

        else:
            # print("\n\ncur index:{},val:{} \nl1 index:{},val:{}\n\n".format(cur_index,li[cur_index],l1_actual_index,li[l1_actual_index]));
            tempVal = li[cur_index];
            li[cur_index] = l1_val;

            li[l1_actual_index] = tempVal;
            l1_cur_swapped_index+=1;
            if (l1_cur_swapped_index >= l1_swapped_length):
                l1_cur_swapped_index = 0;

            num_l1-=1;

        # both update the cur index
        cur_index+=1;


    if (cur_index != l2_e):
        mergeStepInPlace(li,l2_s,l2_s+l1_cur_swapped_index,l2_s+l1_swapped_length);

    return li;


def generateDepGraph(relate_li,dep_list,libToIndex):

    result = dep_list;
    for lib, dep in relate_li:
        result.setdefault(lib, []).append(dep);

    for lib,dep in relate_li:
        if dep not in result:
            result.setdefault(dep,[]);

    count = 0;
    for lib,dep in result.iteritems():
        libToIndex[lib] = count;
        count+=1;

    depGraph = [[0 for i in range(len(result))] for i in range(len(result))];

    for lib,deps in result.iteritems():
        for dep in deps:
            libIndex = libToIndex[lib];
            depIndex = libToIndex[dep];
            depGraph[libIndex][depIndex] = (lib,dep);

    return depGraph;

def invertDic(d):
    newDic = {};
    for k,v in d.iteritems():
        newDic[v] = k;
    return newDic;


def findEmpty(graph,mutate=False):
    foundEmpty = -1;
    for i in range(len(graph)):
        nonzero = 0;
        alreadyDone = False;
        for j in range(len(graph[i])):
            if (graph[i][j] == -1):
                alreadyDone = True;
                break;
            if (graph[i][j]):
                nonzero+=1;
                break;
        if (alreadyDone):
            continue;
        if nonzero == 0:
            foundEmpty = i;
            break;
    if (mutate):
        # flip -1 so you ignoren ext time
        for j in range(len(graph[foundEmpty])):
            graph[foundEmpty][j] = -1;
    
    return foundEmpty;

def buildOrder(relate_li):
    dep_list = {};
    libToIndex = {};
    graph = generateDepGraph(relate_li,dep_list,libToIndex);
    IndexToLib = invertDic(libToIndex);

    build_li = [];

    while (findEmpty(graph) != -1):
        nextBuildIndex = findEmpty(graph,True);

        build_li.append(IndexToLib[nextBuildIndex]);

        # delete all edges to the nextBuildIndex

        for i in range(len(graph)):
            if (graph[i][nextBuildIndex] != 0 and graph[i][nextBuildIndex] != -1):
                x = (graph[i][nextBuildIndex]);
                lib,dep = x;
                if dep == IndexToLib[nextBuildIndex]:
                    graph[i][nextBuildIndex] = 0;

    return build_li;


def getSumSquared(graph,i,j):
    return graph[i][j];

def setSumSquared(graph,val,i,j):
    for row in range(i,len(graph)):
        for col in range(j,len(graph[0])):
            graph[row][col] += val;
    return graph;

class Node:

    def __init__(self,left,right,val,lb,ub):
        self.left = left;
        self.right = right;
        self.val = val;
        self.lb = lb;
        self.ub = ub;


    def __init__(self,left,right,val):
        self.left = left;
        self.right = right;
        self.val = val;  




# returns a tree
def createBST(num_list,lb,ub,rangeDict):

    if (len(num_list) == 0):
        # leaf node where we figure out if its a hole or a mastercard
        if (lb,ub) in rangeDict:

            # the val in the leaf is the actual card
            cur_card = rangeDict[(lb,ub)];

            leaf_n = Node(None,None,cur_card,lb,ub);
            return leaf_n;
        else:

            print("list:{} lb:{} ub:{}".format(num_list,lb,ub));
            return;
    else:
        # recurse cut in half
        midPoint = len(num_list)/2;
        midVal = num_list[midPoint];

        left_li = num_list[:midPoint];
        leftSide = createBST(left_li,lb,midVal,rangeDict);

        right_li = num_list[midPoint+1:];
        rightSide = createBST(right_li,midVal,ub,rangeDict);

        # the midval is used to make the branching BST decision

        inter_n = Node(leftSide,rightSide,midVal,lb,ub);
        return inter_n;

def createRangeDict(card_ranges):
    result = {};
    for (card,(lb,ub)) in card_ranges.iteritems():
        result[(lb,ub)] = card;
    return result;

def flattenRanges(card_ranges):
    li = [];
    for (card,(lb,ub)) in card_ranges.iteritems():
        li.append(lb);
        li.append(ub);
    return li;

def identifyCardRange(card_ranges,li):

    rangeDict = createRangeDict(card_ranges);

    num_list = flattenRanges(card_ranges);

    num_list.sort();
    if (len(num_list) > 0):
        min_val1 = min(num_list);
        max_val1 = max(num_list);
    else:
        return [];

    rangeBST = createBST(num_list,min_val1,max_val1,rangeDict);

    printTree(rangeBST);

    card_li = [];

    for num in li:
        card = findCard(rangeBST,num);
        card_li.append(card);

    return card_li;

def findCard(bst,val):

    # empty
    if (not bst):
        return None;

    # leaf node
    if (not bst.left and not bst.right):
        #print("cur_val:{} bound:{}.{}".format(rangeBST.val,rangeBST.lb,rangeBST.ub));
        if (bst.ub > val and bst.lb <= val):
            return bst.val;

        else:
            return None;
    else:
        if val >= bst.val:
            return findCard(bst.right,val);
        else:
            return findCard(bst.left,val);


def printTree(rangeBST):
    if rangeBST:

        if (not rangeBST.left and not rangeBST.right):
            print("cur_val:{} bound:{}.{}".format(rangeBST.val,rangeBST.lb,rangeBST.ub));
            return;
        else:
            print("{}:{}".format(rangeBST.lb,rangeBST.ub));
            printTree(rangeBST.left);
            printTree(rangeBST.right);
            return;
    else:
        print("the null village");



# [baa,abcd,abca,cad,cab]

# b a c

# d a

# d b

# all pairs a particular ordering how to consolidate

# b,a
# b,c
# a,c
# d,a
# d,b

# d > b > a > c

# d > b
# d > a
# d > c

# b > a
# b > c 

# a > c

def alienOrdering(word_li):

    pair_li = makePairs(word_li,0);

    letters = set();

    letterToIndex = dict();

    graph = makePairGraph(pair_li,letters,letterToIndex);

    indexToLetter = invertDic(letterToIndex);

    ordering = [];

    while (findEmpty(graph) != -1):
        nextIndex = findEmpty(graph,True);

        ordering.append(indexToLetter[nextIndex]);

        # delete all edges to the nextBuildIndex

        for i in range(len(graph)):
            if (graph[i][nextIndex] != 0 and graph[i][nextIndex] != -1):
                x = (graph[i][nextIndex]);
                graph[i][nextIndex] = 0;

    return ordering;




# edge from [d][b] from d -> b d is less than b. since nothing is greater than d. then d has no outgoing edges
# thus you delete every edge where d is the sink of and add d as the start of the order

# how to process this is using an adjacency list which is a dictionary mapped to a set
# for each letter check if it is in the adjacency list. if it has no outgoing edges add it
# to the ordering than reach inside and delete the incoming edges to d.

def makePairGraph(pairs,letters,letterToIndex):
    for a,b in pairs:
        letters.add(a);
        letters.add(b);

    i = 0;
    for letter in letters:
        letterToIndex[letter] = i;
        i+=1;



    graph = [[0 for i in range(len(letters))] for i in range(len(letters))];

    # edge from b -> d if b is less than d
    for a,b in pairs:
        graph[letterToIndex[a]][letterToIndex[b]] = 1;

    return graph;

def makePairGraph(pairs):
    graph = dict();
    for a,b in pairs:
        graph.setdefault(a,set()).add(b);
    return graph;



# returns list of pairs
# pair b,a is if b is less than a
def makePairs(word_li,index):
    if (len(max(word_li)) < index):
        return [];

    if (len(word_li) <= 1):
        return [];

    pair_list = [];
    last_val = "";
    start = 0;
    i = 0;
    for word in word_li:
        if (len(word) <= index):
            continue;

        if (word[index] != last_val and last_val != ""):

            #print("{}\nINDEX:{} {}:{} val {}:{}".format(word_li,index,start,i,last_val,word[index]));

            pair_list.append((word[index],last_val));

            # send the words in the middle recursively
            pair_list += makePairs(word_li[start:i],index+1);

            last_val = word[index];
            start = i;
        else:
            last_val = word[index];

        i+=1;

    # send the words in the middle recursively
    pair_list += makePairs(word_li[start:i],index+1);

    return pair_list;

def createGraph(graph,li,numIndent,curParent):
    if (len(li) == 0):
        return 0
    i = 0
    while (i < len(li)):
        curIndent = li[i].count(" ")
        entry = li[i]
        if curIndent == numIndent+2:
            prevEntry = li[i-1]
            prevIndent = li[i-1].count(" ")
            i+=createGraph(graph,li[i:],prevIndent,prevEntry)

        elif curIndent == numIndent+1:
            graph.setdefault(curParent.strip(),set()).add(entry.strip())
            i+=1
        else:
            return i

    return i


def DFS(graph,curNode,curPath):
    path_li = []
    for entry in graph[curNode]:
        if (entry in graph):
            path_li+=DFS(graph,entry,curPath + "/"+entry)
        else:
            full_path = curPath + "/"+ entry.strip()
            if "." in entry:
                extension = entry.split(".")[-1]
                pic_extensions = set(["gif","jpeg"])
                if extension in pic_extensions:
                    path_li.append(full_path)

    return path_li


def solution(S):
    entryLi = S.split("\n")
    graph = dict()
    createGraph(graph,entryLi,-1,"/")

    path_li = DFS(graph,"/","")

    print(path_li)
    total_len = 0
    for path in path_li:
        total_len += len(path)

    return total_len


def fillBucket(li):

    range_li = []
    
    maxLeft = 0
    for i in range(len(li)):
        if li[i] > maxLeft:
            maxLeft = li[i]
        range_li.append(maxLeft)

    maxRight = 0
    for i in range(len(li)-1,-1,-1):
        if li[i] > maxRight:
            maxRight = li[i]

        range_li[i] = min(range_li[i],maxRight)

    total_sum = 0
    for i in range(len(li)):
        total_sum+=(range_li[i] - li[i])

    return total_sum

def list_addition(add1,add2):

    carryBit = [0 for i in range(max(len(add1),len(add2)) + 1)]
    bigger = add1 if len(add1) > len(add2) else add2
    smaller = add1 if len(add1) <= len(add2) else add2

    output = [0 for i in range(max(len(add1),len(add2)))]
    for i in range(max(len(add1),len(add2))-1,-1,-1):
        if i < len(smaller):
            sum_t = bigger[i] + smaller[i] + carryBit[i+1]
            if sum_t >= 10:
                carryBit[i] = sum_t / 10
            output[i] = str(sum_t % 10)

    strNum = str(carryBit[0]) + "".join(output)
    return int(strNum)

# we can also memoize the values
def maxSumPath(tree_n):
    if (tree_n == None):
        return 0

    if not tree_n.left and not tree_n.right:
        return tree_n.val
    else:
        return max(tree_n.val + maxSumPath(tree_n.left),tree_n.val + maxSumPath(tree_n.right))

# make change problem
# minimum number given list of x coins for y change




def main():
    print("we have begun\n");
    # count = coinCount([5,10,25],35);
    # print(count);

    # permutationString("abc","");

    # permuteBits(4,"");

    # combNofK("abcd",3,"");

    # assert(isOneDelete("abcd","abc") == True);
    # assert(isOneDelete("abdc","abc") == True);
    # assert(isOneDelete("adbc","abc") == True);
    # assert(isOneDelete("dabc","abc") == True);
    # assert(isOneDelete("dbac","abc") == False);

    # word_list = ["bazz","blaze","blaz","blaaz","baz","blz","bllaze","fellow","bllzer","bz","b"];
    
    # len_chain = longestDictionaryChain(word_list);
    # print("{}".format(len_chain));

    # friend_lists = dict();
    # friend_lists["a"] = ["b","c"];
    # friend_lists["b"] = ["a","e"];
    # friend_lists["c"] = ["a","d"];
    # friend_lists["d"] = ["c"];
    # friend_lists["e"] = ["b"];
    # friend_lists["f"] = ["g","h"];
    # friend_lists["g"] = ["f"];
    # friend_lists["h"] = ["f"];

    # # biggest_fg = connectedFriend(friend_lists);
    # # print(biggest_fg);

    # biggest_group = getBiggestFriendGroups(friend_lists);
    # print(biggest_group);

    # l1 = [1,3,5,7];
    # l2 = [2,4,6];
    # newList = mergeStep(l1,l2);
    # print(newList);


    # li = [21,24,37,48,56,7,8,9,101,2578];
    # mergeStepInPlace(li,0,5,9);
    # print(li);

    # relate_li = [("numpy","python"),("tensorflow","numpy"),("tensorflow","scipy"),("scipy","python")];
    # build_order = buildOrder(relate_li);

    # graph = [[0 for i in range(5)] for i in range(5)];
    # setSumSquared(graph,40,2,2);
    # setSumSquared(graph,30,1,1);
    # setSumSquared(graph,10,2,3);
    # print(graph);

    # card_ranges = {"visa":(0000,3333),"mastercard":(5555,7777),"blaze":(8888,9999)};
    # cn_list = [0000,3332,5555,7776,9000];
    # card_list = identifyCardRange(card_ranges,cn_list);
    # print(card_list);


    # word_li = ["baa","abcd","abca","cad","cab"];
    # order = alienOrdering(word_li);

    # print(order);
#     graph = dict()
#     dirString ='''dir1
#  dir11
#   file1.gif
#   file2.txt
#  dir12
#   file3.gif
#   file4.txt
# dir2
#  dir21
#   file5.gif
#   file6.txt
#   dir211
#    file7.gif
#  dir22
#   file8.txt'''

#     total_len = solution(dirString)
#     print(total_len)
    # x = [2,5,1,2,3,4,7,7,6]
    # total_sum = fillBucket(x)
    # print(total_sum)

    add1 = [9,2,3,8]
    add2 = [1,2,3,4]
    sum_t =list_addition(add1,add2)
    print(sum_t)


if __name__ == "__main__":
    main()

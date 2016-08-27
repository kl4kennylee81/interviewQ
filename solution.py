""" Given a file system represented as a String S
return the sum of the length of the full path of all image files
image files being .jpeg and .gif extensions """
def solution(S):
    entryLi = S.split("\n")
    graph = dict()
    createGraph(graph,entryLi,-1,"/")

    path_li = DFS(graph,"/","")
    total_len = 0
    for path in path_li:
        total_len += len(path)

    return total_len

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

def main():
    graph = dict()
    dirString ='''dir1
 dir11
  file1.gif
  file2.txt
 dir12
  file3.gif
  file4.txt
dir2
 dir21
  file5.gif
  file6.txt
  dir211
   file7.gif
 dir22
  file8.txt'''

    total_len = solution(dirString)
    assert(total_len == 91)



if __name__ == "__main__":
    main()


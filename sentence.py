import collections
import fileinput




if __name__ == "__main__":
    sentences = []
    for line in fileinput.input():
        sentences+=line.strip().split(".")
        output = ""
    for sentence in sentences:
        words = sentence.count(" ") + 1
        output+="{} ({}) ".format(sentence,words)
    print(output)

import wikipedia

hendrix = wikipedia.page("Jimmy Hendrix")


#print hendrix.content
#print "\n\n\n"
firstSplit = hendrix.content.split("==")

pageContent = [['Summary', firstSplit[0]]]

for i in range(1,len(firstSplit), 2):
    topic = firstSplit[i]
    content = firstSplit[i+1]
    pageContent.append([topic, content])




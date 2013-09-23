import nuke
import nukescripts

def AE_Transform(AE_Text):
	file = AE_Text
	splitFile = file.splitlines()


	fileWithLineNumbers = zip(range(len(splitFile)), splitFile)
	numberOfLines = len(fileWithLineNumbers)

	positionData = []
	scaleData = []
	rotationData = []

	for i in range(numberOfLines):

		if "Source Width" in fileWithLineNumbers[i][1]:
			sWidth = float(fileWithLineNumbers[i][1].split()[-1])

		elif "Source Height" in fileWithLineNumbers[i][1]:
			sHeight = float(fileWithLineNumbers[i][1].split()[-1])

		elif "Position" in fileWithLineNumbers[i][1]:
			positionLineNumber = fileWithLineNumbers[i][0]
			if "Position" in fileWithLineNumbers[i][1]:
				for aPosItem in fileWithLineNumbers[positionLineNumber+2:]:
					if aPosItem[1] == "":
						break
					else:
						positionData.append(aPosItem[1].strip().split("\t"))   

		elif "Scale" in fileWithLineNumbers[i][1]:
			scaleLineNumber = fileWithLineNumbers[i][0]
			if "Scale" in fileWithLineNumbers[i][1]:
				for aSclItem in fileWithLineNumbers[scaleLineNumber+2:]:
					if aSclItem[1] == "":
						break
					else:
						scaleData.append(aSclItem[1].strip().split("\t"))   

		elif "Rotation" in fileWithLineNumbers[i][1]:
			rotationLineNumber = fileWithLineNumbers[i][0]
			if "Rotation" in fileWithLineNumbers[i][1]:
				for aRotItem in fileWithLineNumbers[rotationLineNumber+2:]:
					if aRotItem[1] == "":
						break
					else:
						rotationData.append(aRotItem[1].strip().split("\t"))


	sNode = nuke.selectedNodes()
	if len(sNode) == 1:
		cNode = sNode[0]
		node = nuke.createNode( 'Transform' )
	else:
		node = nuke.nodes.Transform()
	
	if len(sNode) == 1:
		if not node.input(0):
			node.setInput(0, sNode)
			
	


#	node = nuke.createNode( 'Transform' )
	p = node['translate']
	s = node['scale']
	r = node['rotate']
	c = node['center']

	if len(positionData) != 0:
		p.setAnimated()
		for i in positionData:
			p.setValueAt(float(i[1])-sWidth/2, float(i[0]), 0)
			p.setValueAt(float(i[2])-sHeight/2, float(i[0]), 1)
			

	if len(scaleData) != 0:
		s.setAnimated()
		for i in scaleData:
			s.setValueAt(float(i[1])/100, float(i[0]), 0)
			s.setValueAt(float(i[2])/100, float(i[0]), 1)

	if len(rotationData) != 0:
		r.setAnimated()
		if rotationData != []:
			for i in rotationData:
				r.setValueAt(float(i[1]), float(i[0]))

	c.setValue(sWidth/2, 0)
	c.setValue(sHeight/2, 1)


def AE_Drop( mimeType, text ):
    
    if 'Adobe' in text:
        AE_Text = text
        if 'Transform' in AE_Text:
	        AE_Transform(AE_Text)
        return True
    else:
        return False

nukescripts.addDropDataCallback(AE_Drop)


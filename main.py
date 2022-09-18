mutable_bytes = bytearray()
import xml.etree.ElementTree as ET
from ByteBuffer import ByteBuffer
import guitarpro
import os
from GP7Parser import GP7parse


def showHeaderRevision(byte_s1,byte_s2,byte_s3,byte_s4):
  print(byte_s1,byte_s2,byte_s3,byte_s4)

def bitwise_and_operation(a,b):
  result_int = int.from_bytes(a, byteorder="big") & int.from_bytes(b, byteorder="big")
  return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

'''def getInteger(byteArray, n):
  return int.from_bytes(byteArray[0+n],"big") | int.from_bytes(byteArray[1+n],"big") << 8 | int.from_bytes(byteArray[2+n],"big") << 16 | int.from_bytes(byteArray[3+n],"big") << 24'''

def getInteger(byteArray, n):
  return int.from_bytes(byteArray[0+n],"big") | int.from_bytes(byteArray[1+n],"big") << 8 | int.from_bytes(byteArray[2+n],"big") << 16 | int.from_bytes(byteArray[3+n],"big") << 24

def getInteger_int(byteArray,n):
  return byteArray[0+n] | byteArray[1+n] << 8 | byteArray[2+n] << 16 | byteArray[3+n] << 24

def getString(arrby, n, n2):
  n3 = 0
  n4 = 0;
  arrc[n2] = []
  #for (int i = 0; i < n2 && (n3 = arrby[n + i] & 0xFF) != 0; ++i) {
  n3 = arrby[n] & 0xFF
  i = 0 
  while ( (i < n2 and not n3 == 0)):
      arrc[i] = n3
      n4 = i + 1
      n3 = arrby[n + i] & 0xFF
  arrc2 = bytearray(n4)
  '''for (n3 = 0; n3 < n4; ++n3) {
      arrc2[n3] = arrc[n3];
  }'''
  for var in range(n4):
    arrc2[n3] = arrc[n3]
  return arrc2.decode(arrby,errors='replace')

def getBytes(arrby, n, n2):
  arrby2 = bytearray(n2)
  '''for (int i = 0; i < n2; ++i) {
      if (arrby.length <= n + i) continue;
      arrby2[i] = arrby[n + i];
  }'''
  for var in range(n2):
    if (len(arrby) <= n + var):
      continue
    arrby2[var] = arrby[n+var]
  return arrby2

def openGPXFile(filename):
  mutable_bytes = []
  with open(filename, 'rb') as tabfile:
    # Read Header - e.g. "BCFZ"
    #byte_s1 = tabfile.read(1)
    #byte_s2 = tabfile.read(1)
    #byte_s3 = tabfile.read(1)
    #byte_s4 = tabfile.read(1)
    header_bytes = tabfile.read(4)
    byte_read = True
    while byte_read:
      byte_read = tabfile.read(1)
      mutable_bytes.append(int.from_bytes(byte_read,"little"))
    #myBytes = tabfile.read()
    return (header_bytes, mutable_bytes)

def loadTab(tabfile):
  (header_bytes, mutable_bytes) = openGPXFile(tabfile)
  return loadTabFile(header_bytes, mutable_bytes)


def debugGPXByteBufferInfo(myGPXByteBuffer):
  print("myGPXByteBuffer Length:", myGPXByteBuffer.length())
  print("myGPXByteBuffer Offset:",myGPXByteBuffer.offset())


def calcHeader(byteArray):
  #byteArray = bytes("BCFZ",encoding="utf-8")
  return (getInteger_int(byteArray,0))

def loadTabFile(header_bytes, mutable_bytes):
  #print(myfileByte[0])
  #print("Test",myfileByte[5:8])
  '''byte_s1 = myfileByte[0].to_bytes(1,"big")
  byte_s2 = myfileByte[1].to_bytes(1,"big")
  byte_s3 = myfileByte[2].to_bytes(1,"big")
  byte_s4 = myfileByte[3].to_bytes(1,"big")
  #print(myfileByte[4:])
  for myByteAdd in myfileByte[4:]:
    #print(myByteAdd)
    #print(myfileByte[myByteAdd])
    mutable_bytes.append(myfileByte[myByteAdd])'''

  #showHeaderRevision(byte_s1,byte_s2,byte_s3,byte_s4)
  myGPXByteBuffer = ByteBuffer(len(mutable_bytes),mutable_bytes)
  #debugGPXByteBufferInfo(myGPXByteBuffer)
  #headerbyte = [byte_s1, byte_s2, byte_s3, byte_s4]
  #header = getInteger(headerbyte,0)
  header = calcHeader(header_bytes)

  if (header == 1397113666):
    arrby = myGPXByteBuffer.readBytes(myGPXByteBuffer.length())
    n2 = 4096
    n3 = 0
    while ((n3 + 3) < len(arrby)):
        if not (getInteger_int(arrby, n3) == 2):
          n3 += n2
          continue
        n4 = n3 + 4
        n5 = n3 + 140
        n6 = n3 + 148
        n7 = 0
        n8 = 0
        byteArrayOutputStream = bytearray()
        n8 += 1
        n7 = getInteger_int(arrby, n6 + 4 * n8)
        while not (n7 == 0):
            n3 = n7 * n2
            byteArrayOutputStream.append(getBytes(arrby, n3, n2));
        n9 = getInteger_int(arrby, n5)
        arrby2 = bytearray()
        if (len(arrby2) < n9):
          n3 += n2
          continue
        print("Call recursive:",getString(arrby, n4, 127))
        loadTabFile(getBytes(arrby2, 0, n9)[0], getBytes(arrby2, 0, n9)[1], getBytes(arrby2, 0, n9)[2], getBytes(arrby2, 0, n9)[3], getBytes(arrby2, 0, n9)[4:])
        #this.fileSystem.add(new GPXFile(getString(arrby, n4, 127), getBytes(arrby2, 0, n9)))

        n3 += n2
  elif (header == 1514554178):
    # Get expected uncompressed length of data
    n10 = getInteger_int(myGPXByteBuffer.readBytes(4),0)
    #print("myGPXByteBuffer Offset:",myGPXByteBuffer.offset())
    #print("n10:",n10)
    byteArrayOutputStream = bytearray()
    docuf = open(os.path.join(os.getcwd(),"mydocu.txt"),"wt") 
    docuf.write("n13,n12,n11,n14,len(arrby),n15\n")
    while (not (myGPXByteBuffer.end()) and myGPXByteBuffer.offset() < n10):
      n11 = 0
      n12 = 0
      n13 = myGPXByteBuffer.readBits(1)
      #docuf.write("n13,n12,n11,n14,len(arrby),n15\n")
      if (n13 == 1):
        n12 = myGPXByteBuffer.readBits(4)
        n11 = myGPXByteBuffer.readBitsReversed(n12)
        n14 = myGPXByteBuffer.readBitsReversed(n12)
        arrby = byteArrayOutputStream
        n15 = len(arrby) - n11
        docuf.write("compressed: {p1}|{p2}|{p3}|{p4}|{p6}".format(p1=n13,p2=n12,p3=n11,p4=n14,p6=n15))
        if (n14 > n11):
          runvar = n11
        else:
          runvar = n14
        docuf.write("=> in uncompressed form: ")
        for i in range(runvar):
          try:
            byteArrayOutputStream.append(arrby[n15 + i])
            try:
              docuf.write("|{p1}".format(p1=arrby[n15 + i].to_bytes(1,'little').decode(encoding="cp1252")))
            except:
              docuf.write("|{p1}".format(p1=arrby[n15 + i].to_bytes(1,'little').decode(encoding="cp437")))
          except IndexError:
            pass
        docuf.write("\n")
        continue
      n12 = myGPXByteBuffer.readBitsReversed(2)
      n11 = 0
      docuf.write("RAW: {p1}|{p2}".format(p1=n13,p2=n12))
      try:
        docuf.write("uncompressed: {p1}|{p2}".format(p1=n13.to_bytes(1,'little').decode(encoding="cp1252"),p2=n12.to_bytes(1,'little').decode(encoding="cp1252")))
      except OverflowError:
        docuf.write("Overflow: {p1}|{p2}".format(p1=n13,p2=n12))
      except:
        docuf.write("uncompressed: {p1}|{p2}".format(p1=n13.to_bytes(1,'little').decode(encoding="cp437"),p2=n12.to_bytes(1,'little').decode(encoding="cp437")))
      for i in range(n12):
        n16 = myGPXByteBuffer.readBits(8)
        byteArrayOutputStream.append(n16)
        docuf.write("\t RAW: {p1}".format(p1=n16))
        try:
          docuf.write("|{p1}".format(p1=n16.to_bytes(1,'little').decode(encoding="cp1252")))
        except OverflowError:
          docuf.write("Overflow: |{p1}".format(p1=n16))
        except:
          docuf.write("|{p1}".format(p1=n16.to_bytes(1,'little').decode(encoding="cp437")))

      docuf.write("\n")
  else:
    raise Exception("This is not a GPX File")
  docuf.write("File closed\n")
  docuf.close()
  output_string = bytearray.decode(byteArrayOutputStream,encoding='cp1250',errors='replace')
  return output_string

''' UNDER DEVELOPMENT

def replaceGPIF(mutable_bytes, artist):

  myGPXByteBuffer = ByteBuffer(len(mutable_bytes),mutable_bytes)
  n10 = getInteger_int(myGPXByteBuffer.readBytes(4),0)
  #print("myGPXByteBuffer Offset:",myGPXByteBuffer.offset())
  #print("n10:",n10)
  byteArrayOutputStream = bytearray()
  while (not (myGPXByteBuffer.end()) and myGPXByteBuffer.offset() < n10):
    n11 = 0
    n12 = 0
    n13 = myGPXByteBuffer.readBits(1)
    if (n13 == 1):
      n12 = myGPXByteBuffer.readBits(4)
      n11 = myGPXByteBuffer.readBitsReversed(n12)
      n14 = myGPXByteBuffer.readBitsReversed(n12)
      arrby = byteArrayOutputStream
      n15 = len(arrby) - n11
      if (n14 > n11):
        runvar = n11
      else:
        runvar = n14
      for i in range(runvar):
        try:
          byteArrayOutputStream.append(arrby[n15 + i])
        except IndexError:
          pass
      continue
    n12 = myGPXByteBuffer.readBitsReversed(2)
    n11 = 0
    for i in range(n12):
      byteArrayOutputStream.append(myGPXByteBuffer.readBits(8))
'''

def saveTabFile(tabfile):
  (header_bytes, mutable_bytes) = openGPXFile(tabfile)
  #loadTabFile(byte_s1, byte_s2, byte_s3, byte_s4, mutable_bytes)
  #myGPXByteBuffer = ByteBuffer(len(mutable_bytes),mutable_bytes)
  ## replaceGPIF(mutable_bytes, artist)
  filename = "{tabfile}_new.gpx".format(tabfile=tabfile)
  with open(filename, 'w+b') as mytabfile:
    mytabfile.write(header_bytes)
    for myByte in mutable_bytes:
      mytabfile.write(myByte.to_bytes(1,"little"))
    mytabfile.close()


'''
with open("test.txt", "wt") as xml_file:
    # Write text or bytes to the file
    xml_file.write(bytearray.decode(byteArrayOutputStream,errors='replace'))
#regex
#print(output_string[12000:20000].split("<GPIF>")[1].split("</GPIF>"))
#print("<GPIF>"+ output_string.split("<GPIF>")[1].split("</GPIF>")[0]+"</GPIF>")
'''



def parseXMLData(output_string):
  try:
    root = ET.fromstring("<?xml"+ output_string.split("<?xml")[1].split("</GPIF>")[0]+"</GPIF>")
    return root
  except:
    print("Error not parseable")

def GetGPMetaData_GP15(file):

  gpstruct = guitarpro.parse(file)
  GPFileMetaData = { 
  "Title": gpstruct.title,
  "SubTitle": gpstruct.subtitle,
  "Artist": gpstruct.artist,
  "Album": gpstruct.album,
  "Words": gpstruct.words,
  "Music": gpstruct.music,
  "WordsAndMusic": "",
  "Copyright": gpstruct.copyright,
  "Tabber": gpstruct.tab,
  "Instructions": gpstruct.instructions,
  "Notices": gpstruct.notice,
}
  return GPFileMetaData

def openAndparseXMLData(file):
  tree = ET.parse(file)
  return tree.getroot()

def createGPMetaData(xmlroot):
  for child in xmlroot[3]:
    #print(child.tag,child.text)
    if child.tag == "Title":
      gpTitle = child.text
    elif child.tag == "SubTitle":
      gpSubtitle = child.text
    elif child.tag == "Artist":
      gpArtist = child.text
    elif child.tag == "Album":
      gpAlbum = child.text
    elif child.tag == "Words":
      gpWords = child.text
    elif child.tag == "Music":
      gpMusic = child.text
    elif child.tag == "WordsAndMusic":
      gpWordsAndMusic = child.text
    elif child.tag == "Copyright":
      gpCopyright = child.text
    elif child.tag == "Tabber":
      gpTabber = child.text
    elif child.tag == "Instructions":
      gpInstructions = child.text
    elif child.tag == "Notices":
      gpNotices = child.text

  GPFileMetaData = { 
    "Title": gpTitle,
    "SubTitle": gpSubtitle,
    "Artist": gpArtist,
    "Album": gpAlbum,
    "Words": gpWords,
    "Music": gpMusic,
    "WordsAndMusic": gpWordsAndMusic,
    "Copyright": gpCopyright,
    "Tabber": gpTabber,
    "Instructions": gpInstructions,
    "Notices": gpNotices,
  }
  return GPFileMetaData

def deleteTempfile(file):
  #print(file)
  os.remove(file)
  os.rmdir(os.path.dirname(file))

def GetGPMetaData_GP(file):
  xml = openAndparseXMLData(file)
  deleteTempfile(file)
  return createGPMetaData(xml)

def GetGPMetaData_GPX(output_string):
  root = parseXMLData(output_string)
  for child in root[1]:
    #print(child.tag,child.text)
    if child.tag == "Title":
      gpTitle = child.text
    elif child.tag == "SubTitle":
      gpSubtitle = child.text
    elif child.tag == "Artist":
      gpArtist = child.text
    elif child.tag == "Album":
      gpAlbum = child.text
    elif child.tag == "Words":
      gpWords = child.text
    elif child.tag == "Music":
      gpMusic = child.text
    elif child.tag == "WordsAndMusic":
      gpWordsAndMusic = child.text
    elif child.tag == "Copyright":
      gpCopyright = child.text
    elif child.tag == "Tabber":
      gpTabber = child.text
    elif child.tag == "Instructions":
      gpInstructions = child.text
    elif child.tag == "Notices":
      gpNotices = child.text

  GPFileMetaData = { 
    "Title": gpTitle,
    "SubTitle": gpSubtitle,
    "Artist": gpArtist,
    "Album": gpAlbum,
    "Words": gpWords,
    "Music": gpMusic,
    "WordsAndMusic": gpWordsAndMusic,
    "Copyright": gpCopyright,
    "Tabber": gpTabber,
    "Instructions": gpInstructions,
    "Notices": gpNotices,
  }
  return GPFileMetaData

def ProcessFolder(path):
  myTabs = []
  for root, directories, file in os.walk(path):
    for file in file:
      if(file.endswith(".gp3") or file.endswith(".gp4") or file.endswith(".gp5")):
        print(os.path.join(root,file))
        print(GetGPMetaData_GP15(os.path.join(root,file)))
        #myTabs.append({"File": file, "Path": root, "Data" : GetGPMetaData_GP15(os.path.join(root,file)),})
      if(file.endswith(".gpx")):
        #print(os.path.join(root,file))
        #print(GetGPMetaData_GPX(loadTab(os.path.join(root,file))))
        myTabs.append({"File": file, "Path": root, "Data" : GetGPMetaData_GPX(loadTab(os.path.join(root,file))),})
      if(file.endswith(".gp")):
        print(os.path.join(root,file))
        #print(GetGPMetaData_GP(GP7parse(os.path.join(root,file))))
        #print({"File": file, "Path": root, "Data" : GetGPMetaData_GP(GP7parse(os.path.join(root,file))),})
        #myTabs.append({"File": file, "Path": root, "Data" : GetGPMetaData_GP(GP7parse(os.path.join(root,file))),})
  return myTabs

def TestStartProcessFolderTabs():
  path = os.path.join(os.getcwd(),"Tabs")
  myTabs = ProcessFolder(path)
  for tab in myTabs:
    print(tab["File"], ":", tab["Data"]["Artist"], " - ", tab["Data"]["Title"])

def TestParseGP4File(file):
  gp4 = guitarpro.parse(file)
  print(GetGPMetaData_GP15(gp4))

def TestParseGP3file(file):
  gp3 = guitarpro.parse(file)
  print(GetGPMetaData_GP15(gp3))

def TestParseGPXFile(file):
  '''
  Parse a gpxfile and print Metadata to console
  '''
  #tabfile = "test.gpx"
  #print(loadTabFile(tabfile))
  print(GetGPMetaData_GPX(loadTab(file)))

def writeUncompressedDataFile(file):
  filename = "{tabfile}_new.txt".format(tabfile=file)
  with open(filename, 'w+t') as mytabfile:
    mytabfile.write(loadTab(file))

# Main
TestStartProcessFolderTabs()

#calcHeader("Test")
# Test Join Path with several Parameters
#print(os.path.join(os.getcwd(),'Tabs','test.gpx'))

# Test 
TestParseGPXFile(os.path.join(os.getcwd(),'Tabs','test.gpx'))

writeUncompressedDataFile(os.path.join(os.getcwd(),'Tabs','test.gpx'))

# TestParseGP4File('GuitarPRO4.gp4')
# TestParseGP3file('GuitarPRO3.gp3') 
# saveTabFile(os.path.join(os.getcwd(),"Tabs","hotelCalifo.gpx"))

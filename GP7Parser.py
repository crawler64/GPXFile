from zipfile import ZipFile
import os
 
def GP7parse(file):
  files = []
  with ZipFile(file, 'r') as zipObj:
  # Get a list of all archived file names from the zip
    listOfFileNames = zipObj.namelist()
    # Iterate over the file names
    for fileName in listOfFileNames:
        # Check filename endswith csv
        if fileName.endswith('.gpif'):
            # Extract a single file from zip
            zipObj.extract(fileName, 'temp')
            files.append(fileName)

  return os.path.join(os.getcwd(),"temp", files[0])

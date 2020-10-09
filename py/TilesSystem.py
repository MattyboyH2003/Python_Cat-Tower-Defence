def GenerateMap(self): #Ran just before game loop to generate the map
        
        #for a tile key, check MapList.py

        mapFile = open(self.currentMap, "r")
        fileContents = mapFile.readlines()
        mapFile.close()
        mapString = ""
        for item in fileContents:
            #mapString += item.replace("\n", "")

        typeList = {
            "#" : Ground,
            "P" : Path,
            ">" : StartRight,
            "<" : StartLeft,
            "/" : StartDown,
            "^" : StartUp,
            "," : EndLeft,
            "6" : EndDown,
            "." : EndRight,
            "?" : EndUp
        }

        counter = 0
        for char in mapString:
            try:
                nextTile = typeList[char]
            except:
                print("Error! Map tile not in typelist")
            location = [((counter%54)*20)+10, ((counter//54)*20)+10]
            tile = nextTile(location, colours["red"])

            self.allSpritesList.add(tile)
            self.tileSpritesList.add(tile)

            if nextTile != Ground:
                self.collisionSpritesList.add(tile)

            counter += 1

        self.GeneratePath()
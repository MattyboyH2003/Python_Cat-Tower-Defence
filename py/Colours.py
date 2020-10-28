#Colours Dictionary
colours = {

    #colours
    "red" : (200, 0, 0),
    "green" : (0, 200, 0),
    "purple" : (255, 0, 255),
    "lavender" : (150, 150, 200),
    "brown" : (139, 69, 19),
    "blue" : (0, 0, 200),
    "sky_blue" : (59, 196, 217),

    #alternative colours
    "bright_lavender" : (150, 150, 255),
    "bright_red" : (255, 0, 0),
    "bright_green" : (0, 255, 0),
    "bright_brown" : (210, 105, 30),
    "bright_blue" : (0, 0, 255),
    "bright_sky_blue" : (117, 237, 255),

    #shades
    "white" : (255, 255, 255),
    "grey"  : (125, 125, 125),
    "black" : (0, 0, 0)
}

def Darken(colour):
    newColour = list(colour)
    for i in range(3):
        newColour[i] += 30
        if newColour[i] >= 255:
            newColour[i] = 255
        elif newColour[i] <= 0:
            newColour[i] = 0
    newColour = tuple(newColour)
    return (newColour)  

def Lighten(colour):
    newColour = list(colour)
    for i in range(3):
        newColour[i] -= 30
        if newColour[i] >= 255:
            newColour[i] = 255
        elif newColour[i] <= 0:
            newColour[i] = 0
    newColour = tuple(newColour)
    return (newColour)  

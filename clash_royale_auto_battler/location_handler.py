import pyautogui

class LocationHandler:

    def __init__(self,base_image_url):
        #locations of images that we've already found
        self.locations = {}
        #the file that the images are kept in
        self.base_image_url = base_image_url

    def get_location(self,image,region=None,confidence=0.95,grayscale = True):
        """finds the image by either locating it on the screen or by looking up its location if it's been located before. returns None if image is not found in locations or on the screen"""
        if image in self.locations.keys():
            print(image+" already found")
            return self.locations[image]
        else:
            print("searching for "+image)
            #we can use the size and location of the screen once we find it to narrow down the source (currently not in use for testing purposes)
            if(region != None):
                center = pyautogui.locateCenterOnScreen(self.base_image_url+image,grayscale = grayscale,region=region,confidence=confidence)
            else:
                center = pyautogui.locateCenterOnScreen(self.base_image_url+image,grayscale = grayscale,confidence=confidence)
            if center != None:
                print("found at "+str(center.x)+","+str(center.y))
                self.locations[image] = center
                return center
            else:
                return None
            
    def get_multiple_locations(self,image):
        """finds all non-duplicate instances of the given image. currently does not do a good job of finding all of them--it usually finds one or two."""
        print("searching for multiple instances of "+image)
        if image in self.locations.keys():
            print(str(len(self.locations[image]))+" copies of "+image+" already found")
            return self.locations[image]
        else:
            #ALGORITHM TO ONLY RETURN NON-DUPLICATE INSTANCES
            #(locateAllOnScreen tends to find the same instance of the same image more than once)
            verified_non_duplicates = []
            #loop through everything locateAllOnScreen finds
            for possible_appearance in pyautogui.locateAllOnScreen(self.base_image_url+image,confidence=0.65):
                not_a_duplicate = True
                #if it's too close to an instance we've already found it must be a duplicate
                for verified_non_duplicate in verified_non_duplicates:
                    if abs(possible_appearance[0] - verified_non_duplicate[0]) < 5:
                        not_a_duplicate = False
                #only add it to the results if it isn't a duplicate of an instance that's already in the results
                if not_a_duplicate:
                    verified_non_duplicates.append(possible_appearance)

            #locateAllOnScreen doesn't return the centers of the images, so we have to extract them
            centers = []
            for verified_non_duplicate in verified_non_duplicates:
                centers.append((verified_non_duplicate[0]+verified_non_duplicate[2]/2,verified_non_duplicate[1]+verified_non_duplicate[3]/2))
            #put the found instances into locations as a list under the key <name of the image>
            self.locations[image] = centers
            print("found "+str(len(centers))+" instances of "+image)
            return self.locations[image]
    
    def forget_location(self,image):
        print("forgetting about "+image)
        self.locations.pop(image,None)

    def reset(self):
        print("forgetting all button locations in case they were incorrect")
        self.locations = {}
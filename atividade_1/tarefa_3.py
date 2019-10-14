# import the necessary packages
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import cv2


# construct the argument parser and parse the arguments

"""
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "Path to the directory of images")
args = vars(ap.parse_args())
"""

# initialize the index dictionary to store the image name
# and corresponding histograms and the images dictionary
# to store the images themselves
index = {}
images = {}



config_heroi = {
        "MODELO": {"Hulk": "Hulk.png", "America": "America.png",\
                   "Batman": "Batman.png", "Ferro": "Ferro.png",\
                   "Flash": "Flash.png", "Maravilha": "Maravilha.png",\
                   "Super": "super.png", "Wolverine": "wolverine.png"},
                   
        "MODELO_HIST": {"Hulk": None, "America": None,\
                        "Batman": None, "Ferro": None,\
                        "Flash": None, "Maravilha": None,\
                        "Super": None, "Wolverine": None},
                   
        "BaseQ": {"QUEM1": "QUEM1.png","QUEM2": "QUEM2.png",\
                  "QUEM3": "QUEM3.png","QUEM4": "QUEM4.png",\
                  "QUEM5": "QUEM5.png",\
                  "QUEM6": "quem6.png","QUEM7": "quem7.png",\
                  "QUEM8": "quem8.png","QUEM9": "quem9.png",\
                  "QUEM10":"quem10.png","QUEM11":"quem11.png",\
                  "QUEM12":"quem12.png","QUEM13": "quem13.png",\
                  "QUEM14":"quem14.png","QUEM15": "quem15.png",\
                  "QUEM16":"quem16.png"
                },
        
        "BaseQ_HIST": {"QUEM1": None,"QUEM2": None,\
          "QUEM3": None,"QUEM4": None,\
          "QUEM5": None,\
          "QUEM6": None,"QUEM7": None,\
          "QUEM8": None,"QUEM9": None,\
          "QUEM10": None,"QUEM11":None,\
          "QUEM12": None,"QUEM13": None,\
          "QUEM14": None,"QUEM15": None,\
          "QUEM16": None}
        }



def carrega_base():
    

    for modelo in config_heroi["MODELO"]:
        image = cv2.imread("Base1/"+ config_heroi["MODELO"][modelo])
        
        config_heroi["MODELO"][modelo] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        # extract a 3D RGB color histogram from the image,
        # using 8 bins per channel, normalize, and update
        # the index
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        config_heroi["MODELO_HIST"][modelo] = hist
    
    
    
    for teste in config_heroi["BaseQ"]:
        image = cv2.imread("BaseQUEM/"+ config_heroi["BaseQ"][teste])
        
        config_heroi["BaseQ"][teste] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        config_heroi["BaseQ_HIST"][teste] = hist



def compara_histogramas():

    OPENCV_METHODS = (
        ("Correlation", cv2.HISTCMP_CORREL),
        ("Chi-Squared", cv2.HISTCMP_CHISQR),
        ("Intersection", cv2.HISTCMP_INTERSECT),
        ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))
   

    results = {}
    

    for (methodName, method) in OPENCV_METHODS:
        
        results[methodName] = {}
    
        for (j, hist2) in config_heroi["BaseQ_HIST"].items():
            
            results[methodName][j] = []            
            for (k, hist) in config_heroi["MODELO_HIST"].items():

                d = cv2.compareHist(hist, hist2, method)
                results[methodName][j].append((k,d))
                
   
    return results
 

def classifica(d):
    
    r = {}

    for methodName in d:
        r[methodName] = {}
        reverse = False
        if methodName in ("Correlation", "Intersection"):
            reverse = True
        for quem in d[methodName]:
            r[methodName][quem] = sorted([(v, k) for (k, v) in d[methodName][quem]], reverse = reverse)[0]
            
    return r        


def input_teste(c):
    
    print("Digite o numero de um QUEM para descobrir qual super heroi é!")
    
    i = 0
    q = []
    for quem in config_heroi["BaseQ"]:
        print("%d- %s "%(i+1, quem))
        q.append(quem)
        i+=1
    r = int(input("Quero saber o QUEM de numero: "))
    
    for methodName in c:
        print("Para o método %s o QUEM %d é: %s"%(methodName.upper(), r, c[methodName][q[r-1]][1]))
        
    
def main():
    
    carrega_base()
    
    r = compara_histogramas()
    
    c = classifica(r)
    
    input_teste(c)
    
if __name__ == "__main__":
    main()
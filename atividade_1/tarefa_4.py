# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 19:21:59 2019

@author: anaru
"""

from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import cv2


config = {
        "MODELO": {"Goblin": ["Goblin_town1.jpg","Goblin_town2.jpg","Goblin_town3.jpg","Goblin_town4.jpg"],
                   "Mordor": ["mordor1.jpg", "mordor2.jpg","Mordor3.png","Mordor4.jpg"],
                   "Rivendell": ["Rivendell1.png", "Rivendell2.jpg", "Rivendell3.jpg", "Rivendell5.jpg"],
                   "Shire": ["Shire1.jpg", "Shire2.jpg", "Shire3.jpg", "Shire5.jpg"]
                   },
                   
        "MODELO_HIST":  {"Goblin": ["Goblin_town1.jpg","Goblin_town2.jpg","Goblin_town3.jpg","Goblin_town4.jpg"],
                   "Mordor": ["mordor1.jpg", "mordor2.jpg","Mordor3.jpg","Mordor4.jpg"],
                   "Rivendell": ["Rivendell1.png", "Rivendell2.png", "Rivendell3.png", "Rivendell5.png"],
                   "Shire": ["Shire1.jpg", "Shire2.jpg", "Shire3.jpg", "Shire5.jpg"]
                   },
                   
        "BaseO": {"ONDE1": "Onde1.jpg","ONDE2": "Onde2.jpg",\
                  "ONDE3": "Onde3.jpg","ONDE4": "Onde4.jpg"
                  }
                  ,
        
        "BaseO_HIST": {"ONDE1": None,"ONDE2": None,\
                       "ONDE3": None,"ONDE4": None}
        }



def carrega_base():
    
    
    
    for lst in config["MODELO"]:
        for i,modelo in enumerate(config["MODELO"][lst]): 
            
            image = cv2.imread("Base3/"+ modelo)
            
            config["MODELO"][lst][i] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            config["MODELO_HIST"][lst][i] = hist
     
        
    
    
    for teste in config["BaseO"]:
        image = cv2.imread("Base3/"+ config["BaseO"][teste])
        
        config["BaseO"][teste] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        config["BaseO_HIST"][teste] = hist




def compara_histogramas():
  
    OPENCV_METHODS = (
        ("Correlation", cv2.HISTCMP_CORREL),
        ("Chi-Squared", cv2.HISTCMP_CHISQR),
        ("Intersection", cv2.HISTCMP_INTERSECT),
        ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))
    	
    SCIPY_METHODS = (("Euclidean", dist.euclidean),
    	("Manhattan", dist.cityblock),
    	("Chebysev", dist.chebyshev))
    
    
    results = {}
    
    for (methodName, method) in OPENCV_METHODS:
   
        results[methodName] = {}
    
        for (j, hist2) in config["BaseO_HIST"].items():
        
            
            results[methodName][j] = {}            
            for item in config["MODELO_HIST"]:
                results[methodName][j][item] = []   
                
                for hist in config["MODELO_HIST"][item]:
                  
                   d = cv2.compareHist(hist, hist2, method)
                   results[methodName][j][item].append(d)


    
    for (methodName, method) in SCIPY_METHODS:
   
        results[methodName] = {}
    
        for (j, hist2) in config["BaseO_HIST"].items():
        
            
            results[methodName][j] = {}            
            for item in config["MODELO_HIST"]:
                results[methodName][j][item] = []   
                
                for hist in config["MODELO_HIST"][item]:
                  
                   d = method(hist, hist2)
                   results[methodName][j][item].append(d)                    
    
    return results


def classifica(d):
    
    r = {}

    for methodName in d:
        r[methodName] = {}
        reverse = False
        if methodName in ("Correlation", "Intersection"):
            reverse = True
        for onde in d[methodName]:
            r[methodName][onde] = {}
    
            #cada classe
            for item in d[methodName][onde]:
                r[methodName][onde][item] = sorted(d[methodName][onde][item], reverse = reverse)[0]
    
    
    n = {}
    for method in r:
        n[method] = {}
        
        reverse = False
        
        if method in ("Correlation", "Intersection"):
            reverse = True
        
        l = []
        
        for onde in r[method]:
            l = []
            for k,v in r[method][onde].items():
                l.append((v,k))

            n[method][onde] = sorted(l, reverse=reverse)[0]
            
    
    return n        


def input_teste(c):
    
    print("Digite o numero de um ONDE para descobrir qual local é!")
    
    i = 0
    q = []
    for onde in config["BaseO"]:
        print("%d- %s "%(i+1, onde))
        q.append(onde)
        i+=1
    r = int(input("Quero saber o ONDE de numero: "))
    print()
    for methodName in c:
        print("Para o método %s o ONDE %d é: %s"%(methodName.upper(), r, c[methodName][q[r-1]][1]))

        
    
def main():
    
    carrega_base()
    
    r = compara_histogramas()
    
    c = classifica(r)

    input_teste(c)
    
if __name__ == "__main__":
    main()
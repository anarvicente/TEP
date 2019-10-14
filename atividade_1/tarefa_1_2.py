#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:05:30 2019

@author: ana
"""

import matplotlib.pyplot as plt
import numpy as np


def return_intersection(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    intersection = np.true_divide(np.sum(minima),np.sum(hist_2))
    return intersection

def mostra_grafico():
       
    x = []
    y = []
    for elem in config_grafico[BASE_TESTE]:
        for e in config_grafico[BASE_TESTE][elem]:
            x.append(e[0])
            y.append(e[1])
#       
            
        img = plt.imread(BASE_TESTE+"/"+config_heroi[BASE_TESTE][elem][0])
        
        
        fig = plt.figure()
        a = fig.add_subplot(221)
        plt.imshow(img)
        a.set_title(elem)
    
        
        a = fig.add_subplot(222)
        
        width = 0.5
        a.barh(x, y, width, color="red")
        plt.show(a)



def calcula_compatibilidade():
    
    for modelo in config_heroi["MODELO"]:
        img = plt.imread(BASE_MODELO+"/"+config_heroi["MODELO"][modelo])
        hr, bins = np.histogram(img[:,:,0], bins=256)
        hg, bins = np.histogram(img[:,:,1], bins=256)
        hb, bins = np.histogram(img[:,:,2], bins=256)
        
        for teste in config_heroi[BASE_TESTE]:
            img2 = plt.imread(BASE_TESTE+"/"+config_heroi[BASE_TESTE][teste][0])    
            hr2, bins = np.histogram(img2[:,:,0], bins=256)
            hg2, bins = np.histogram(img2[:,:,1], bins=256)
            hb2, bins = np.histogram(img2[:,:,2], bins=256)
                    
            r = return_intersection(hr, hr2)
            g = return_intersection(hg, hg2)
            b = return_intersection(hb, hb2)
        
            comp = r + g + b
            
            #dividi por 3 para a probabilidade ficar entre 0 e 1
            config_grafico[BASE_TESTE][teste].append((modelo,comp/3))
            
            #se usar uma flag MAIOR, pergunta sera:
            #entre esses 5, qual o maior? 
            #ai o QUEM3 sempre sera o maior,exceto pro batman
            #Pergunta: entre todos os 1, qual o maior?
            
            if comp > config_heroi[BASE_TESTE][teste][1]:
                config_heroi[BASE_TESTE][teste][1] = comp
                config_heroi[BASE_TESTE][teste][2] = modelo


    
config_heroi = {
        "MODELO": {"Hulk": "Hulk.png", "America": "America.png",\
                   "Batman": "Batman.png", "Ferro": "Ferro.png",\
                   "Flash": "Flash.png", "Maravilha": "Maravilha.png",\
                   "Super": "super.png", "Wolverine": "wolverine.png"},
                   
        "Base1": {"QUEM1": ["QUEM1.png",0,""],"QUEM2": ["QUEM2.png",0,""],\
                  "QUEM3": ["QUEM3.png",0,""],"QUEM4": ["QUEM4.png",0,""],\
                  "QUEM5": ["QUEM5.png",0,""]},
                  
        "Base2": {"QUEM6": ["quem6.png", 0,""],"QUEM7": ["quem7.png", 0,""],\
                  "QUEM8": ["quem8.png", 0,""],"QUEM9": ["quem9.png", 0,""],\
                  "QUEM10":["quem10.png", 0,""],"QUEM11":["quem11.png", 0,""],\
                  "QUEM12":["quem12.png", 0,""],"QUEM13": ["quem13.png", 0,""],\
                  "QUEM14":["quem14.png", 0,""],"QUEM15": ["quem15.png", 0,""],\
                  "QUEM16":["quem16.png", 0,""]
                }
        }


    
config_grafico = {
        
        "Base1": {"QUEM1": [],"QUEM2": [],\
                  "QUEM3": [],"QUEM4": [],\
                  "QUEM5": []},
                  
        "Base2": {"QUEM6": [],"QUEM7": [],\
                  "QUEM8": [],"QUEM9": [],\
                  "QUEM10":[],"QUEM11":[],\
                  "QUEM12":[],"QUEM13":[],\
                  "QUEM14":[],"QUEM15":[],\
                  "QUEM16":[]}
        
        }
   
BASE_TESTE = "Base1"  #poder ser Base1 ou Base2
BASE_MODELO = "Base1" #sempre eh Base1 pq os arquivos modelo estao dentro dessa pasta

def main():
    
    print("Calculando compatibilidade..")
    calcula_compatibilidade()
    
    print(config_heroi["Base1"])
    
    mostra_grafico()
 
    
if __name__ == '__main__':
    main()


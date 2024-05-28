# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:33:49 2023

@author: Rik
"""

import wis_2_2_utilities as util
import wis_2_2_systems as systems
import matplotlib.pyplot as plt
# import pandas as pd #Deze code alleen gebruiken indien pandas geïnstalleerd

#set timestep
timestep = 2e-3

# Controller inleveropdracht 1
class controller():
    def __init__(self, target=0):
       #Positie en snelheid #vliegwiel
        self.target = target
        self.Integral1 = 0.
        self.K_P1 = 0
        self.K_I1 = 0
        self.K_D1 = 0.2
        
       #Hoek en hoeksnelheid #slinger
        self.Integral2 = 0.
        self.K_P2 = -150
        self.K_I2 = 0
        self.K_D2 = -40
        
    def feedBack(self, observe):
        #update integral term
        self.Integral1 += observe[0]*timestep
        self.Integral2 += observe[2]*timestep
        #calculate feedback
        u=self.K_P1*observe[0]+\
        self.K_I1*self.Integral1+\
        self.K_D1*observe[1]+\
        self.K_P2*observe[2]+\
        self.K_I2*self.Integral2+\
        self.K_D2*observe[3]
        
        return u

# def Dataplot(): #Deze code alleen gebruiken indien pandas geïnstalleerd
#     """
#     Created on Thur 16-11-2023 15:24

#     @author: Nathan
#     """

#     # Read the data
#     data = pd.read_csv('flywheel_inverted_pendulum.csv', sep=',')
    
#     # Define your column names
#     column_names = ['tijd', 'kwad_toestand_kosten', 'kwad_input_kosten', 'hoek_vliegwiel','hoeksnelheid_vliegwiel','hoek_slinger_1','hoeksnelheid_slinger_1','input'] 
    
#     # Assign the column names to the DataFrame
#     data.columns = column_names
    
#     tijd = data['tijd']
#     toestand_kosten = data['kwad_toestand_kosten']
#     input_kosten = data['kwad_input_kosten']
#     hoek_v = data['hoek_vliegwiel']
#     hoeksnelheid_v = data['hoeksnelheid_vliegwiel']
#     hoek_s = data['hoek_slinger_1']
#     hoeksnelheid_s = data['hoeksnelheid_slinger_1']
#     inputs = data['input']
        
#     #plot
#     plt.plot(tijd, inputs)
#     plt.xlabel('Tijd(s)')
#     plt.ylabel('Input')
#     plt.title('')
#     plt.show()
    
#     #plot
#     plt.plot(tijd, hoeksnelheid_s)
#     plt.xlabel('Tijd(s)')
#     plt.ylabel('Snelheid slinger')
#     plt.title('')
#     plt.show()
    
#     #plot
#     plt.plot(tijd, hoeksnelheid_v)
#     plt.xlabel('Tijd(s)')
#     plt.ylabel('Snelheid vliegwiel')
#     plt.title('')
#     plt.show()
    
#     #plot
#     plt.plot(tijd,toestand_kosten)
#     plt.xlabel('Tijd(s)')
#     plt.ylabel('Kwadratische toestands kosten')
#     plt.title(max(toestand_kosten))
#     plt.show()

def main():
  model=systems.flywheel_inverted_pendulum()
  control = controller()
  simulation = util.simulation(model=model,timestep=timestep)
  simulation.setCost()
  simulation.max_duration = 10 #seconde
  simulation.GIF_toggle = False  #set to false to avoid frame and GIF creation


  while simulation.vis.Run():
      if simulation.time<simulation.max_duration:
        simulation.step()
        u = control.feedBack(simulation.observe())
        simulation.control(u)
        simulation.log()
      else:
        print('Ending visualisation...')
        simulation.vis.GetDevice().closeDevice()
    
        
  simulation.writeData()
  # Dataplot() #Deze code alleen gebruiken indien pandas geïnstalleerd
        
if __name__ == "__main__":
  main()
# Starting the threads
from regulator import Regulator
from CFClient import CFClient
from threading import Thread
from GUI import GUI, plotting, fig
from matplotlib import animation
import cflib
import time
from referenceGenerator import ReferenceGenerator
#from GUI import MyFirstGUI

URI = 'radio://0/80/2M' # Link to the radio
# Starting some threads
cflib.crtp.init_drivers(enable_debug_driver=False)

# The regulator thread is started when the connection is set up
regul = Regulator(URI)

ref_gen = ReferenceGenerator(regul)
ref_gen.start()
# GUI
gui = GUI()
gui.set_ref_gen(ref_gen)
gui.set_regul(regul)
#Starting the plotting thread
plotting_period =300 # In ms
z_ani1=animation.FuncAnimation(fig, plotting, fargs=(gui,), interval=plotting_period)
gui.mainloop()

while True:
    pass

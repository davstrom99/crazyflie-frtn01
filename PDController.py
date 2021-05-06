import threading

class PDController:
    def __init__(self, h, static_gain=0):
        # Private variables
        self.v = 0 # Output from controller

        # Control variables
        self.K = 0
        self.h = h # period in ms
        self.Td = 0
        self.N = 0 #Maximum derivative gain, often between 5 and 20., 7

        self.y = 0 # Measurement signal
        self.yOld = 0 # Old measurement signal
        self.e = 0 # Error
        self.D = 0 # Derivative part of the controller
        self.ad = 0
        self.bd = 0
        self.static_gain = static_gain

        self._lock = threading.Lock()

    def calc_out(self, y, y_ref):
        with self._lock:
            self.y = y
            #eOld = self.e
            self.e = y_ref - y

            self.D = self.ad*self.D - self.bd*(y-self.yOld)
            #self.D = self.ad*self.D + self.bd*(self.e - eOld);
            self.v = self.K *(y_ref - y) + self.D+self.static_gain

        return self.v

    def update_state(self,u):
        with self._lock:
            self.ad = self.Td / (self.Td + self.N*self.h);
            self.bd = self.K*self.ad*self.N;

            self.yOld = self.y;

    def set_params(self, **kwargs):
        with self._lock:
            self.K = kwargs.get('K', self.K)
            self.h = kwargs.get('h',self.h)
            self.Td = kwargs.get('Td',self.Td)
            self.N = kwargs.get('N',self.N)

            self.ad = self.Td / (self.Td + self.N*self.h);
            self.bd = self.K*self.ad*self.N;

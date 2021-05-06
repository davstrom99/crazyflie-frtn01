import threading
import time


class ReferenceGenerator(threading.Thread):
    def __init__(self,regul):
        threading.Thread.__init__(self)
        self.regulator=regul
        self.trajectory = ""

        # Setting up trajectories
        self.back_n_forth_starting_point = [0,0,0.3]
        self.back_n_forth_starting_point_duration = 5
        self.back_n_forth_setpoints = [[0.3,0,0.3],[0,0,0.3]]
        self.back_n_forth_timing = [7,7] # Duration to wait for the drone to converge to each setpoint

        self.vert_square_starting_point = [0,0,0.5]
        self.vert_square_starting_point_duration = 4
        self.vert_square_setpoints = [[0.5,0,0.5],[0.5,0,1],[0,0,1],[0,0,0.5]]
        self.vert_square_timing = [4,4,4,4]

    def set_trajectory(self, trajectory):
        """A trajectory can also be set by calling 'objectname'.trajectory= "..." from outside.
        This method is only intentended to make the structure of the class clear."""
        self.trajectory = trajectory


    def run(self):
        running = False
        while True:
            tid =time.time()
            if self.trajectory == "back_n_forth":
                running = True
                self.regulator.ref = self.back_n_forth_starting_point
                time.sleep(self.back_n_forth_starting_point_duration)
                while self.trajectory == "back_n_forth":
                    """Moves back and forth in 7 second intervals"""
                    self.regulator.ref = self.back_n_forth_setpoints[0]
                    time.sleep(self.back_n_forth_timing[0])
                    self.regulator.ref = self.back_n_forth_setpoints[1]
                    time.sleep(self.back_n_forth_timing[1])
            elif self.trajectory == "vert_square":
                running = True
                self.regulator.ref = self.vert_square_starting_point
                time.sleep(self.vert_square_starting_point_duration)
                while self.trajectory == "vert_square":
                    """Moves in a vetical square during 16 seconds"""
                    self.regulator.ref = self.vert_square_setpoints[0]
                    print("Ett")
                    time.sleep(self.vert_square_timing[0])
                    self.regulator.ref = self.vert_square_setpoints[1]
                    print("Två")
                    time.sleep(self.vert_square_timing[1])
                    print("Tre")
                    self.regulator.ref = self.vert_square_setpoints[2]
                    time.sleep(self.vert_square_timing[2])
                    print("Fyra")
                    self.regulator.ref = self.vert_square_setpoints[3]
                    time.sleep(self.vert_square_timing[3])
                    print("Fem")
            else:
                running = False
            if not running:
                # Waiting for someone to set a trajectory
                time.sleep(3)

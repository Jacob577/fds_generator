import os
import keyboard
import time
import psutil

class Main:

    def __init__(self, iteration):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.iteration = iteration
        self.fds_file = ""

    def create_directory(self):
        directory = self.path + "/folder{}".format(self.iteration)
        os.mkdir(directory)

    def create_file(self, mass_flux):
        f = open("test{}.fds".format(self.iteration), "w")
        self.fds_file = Main(self.iteration).create_fds(mass_flux=mass_flux)
        f.write(self.fds_file)
        f.close()
        os.system("move " + self.path + "\\test{}.fds ".format(self.iteration) + self.path +
                  "\\folder{}".format(self.iteration))

        os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\FDS6\\CMDfds.lnk")
        time.sleep(2)
        keyboard.write("cd " + self.path + "\\folder{}".format(self.iteration))
        keyboard.press("enter")
        keyboard.write("fds " + "test{}.fds".format(self.iteration))
        keyboard.press("enter")


    def create_fds(self, mass_flux):
        self.fds_file = '''
&HEAD CHID='circular_burner', TITLE='Test the mass flow rate from a circular burner' /

&MULT ID='mesh array', DX=1.0,DY=1.0,DZ=1.0, I_UPPER=1,J_UPPER=1,K_UPPER=1 /
&MESH IJK=20,20,20, XB=-1.0,0.0,-1.0,0.0,0.0,1.0, MULT_ID='mesh array' /

&TIME T_END=20. /

&REAC FUEL='PROPANE', SOOT_YIELD=0.015 /

&SURF ID='BURNER', MASS_FLUX(1)={}, SPEC_ID(1)='PROPANE', TAU_MF(1)=0.01 /

&VENT XB=-0.6,0.6,-0.6,0.6,0,0, XYZ=0,0,0, RADIUS=0.5, SPREAD_RATE=0.05, COLOR='BLUE', SURF_ID='BURNER' /

&VENT MB='ZMAX',SURF_ID='OPEN'/
&VENT MB='YMIN',SURF_ID='OPEN'/
&VENT MB='YMAX',SURF_ID='OPEN'/
&VENT MB='XMIN',SURF_ID='OPEN'/
&VENT MB='XMAX',SURF_ID='OPEN'/

&DUMP DT_HRR=0.1 /

&SLCF PBY=0.0, QUANTITY='TEMPERATURE' /

&TAIL /
        '''.format(mass_flux)
        return self.fds_file


if __name__ == '__main__':
    count = 0
    for i in range(5):
        Main(iteration=i).create_directory()
        Main(iteration=i).create_file(i*0.1)
        count += 1
        time.sleep(5)
        if count >= 3:
            not_again = True
            while not_again:
                time.sleep(30)
                utilization = psutil.cpu_percent()
                if float(utilization) > 60:
                    not_again = True
                else:
                    not_again = False
                    count = 0



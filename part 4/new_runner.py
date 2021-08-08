from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import pandas as pd
import numpy as np
import math

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

column_names = [(str(n1) + 'to' + str(n2)) for n1 in range(1, 9) for n2 in range(1, 9) if n1 != n2]
cols = [('S0PhaseTime' + str(i)) for i in range(1, 7)] + [('S1PhaseTime' + str(i)) for i in range(1, 5)] + \
       [('S2PhaseTime' + str(i)) for i in range(1, 7)] + [('S3PhaseTime' + str(i)) for i in range(1, 4)] + \
       [('SS' + str(i) + 'PhaseTime1') for i in range(4)]

def open_data(name):
    filename = 'input' + os.sep + name
    # column_names = [(str(n1) + 'VOEM' + str(n2) + 'n') for n1 in range(4) for n2 in range(1, 13)]
    data = pd.read_csv(filename, usecols=column_names)
    data.applymap(lambda x: math.floor(x))
    return data


def generate_routefile(data, Num):
    OD = data

    with open(('data' + os.sep + 'fyp' + str(Num) + '.rou.xml'), 'w') as routes:
        print(
            """
            <routes>
            <vType id="car" accel="2.4" decel="4.0" sigma="0.5" length="5.5" minGap="2.5" maxSpeed="16.67"/>
            
            <route id="1to2" edges="gn1_n1 n1_a1 a1_j1 j1_d4 d4_d5 d5_n2 n2_gn2" />
            <route id="1to3" edges="gn1_n1 n1_a1 a1_j1 j1_a2 a2_a3 a3_j2 j2_f1 f1_f2 f2_n3 n3_gn3" />
            <route id="1to4" edges="gn1_n1 n1_a1 a1_j1 j1_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_h3 h3_n4 n4_gn4" />
            <route id="1to5" edges="gn1_n1 n1_a1 a1_j1 j1_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_a6 a6_a7 a7_j4 j4_n5 n5_gn5" />
            <route id="1to6" edges="gn1_n1 n1_a1 a1_j1 j1_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_a6 a6_a7 a7_j4 j4_n6 n6_gn6" />
            <route id="1to7" edges="gn1_n1 n1_a1 a1_j1 j1_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_g2 g2_n7 n7_gn7" />
            <route id="1to8" edges="gn1_n1 n1_a1 a1_j1 j1_c3 c3_n8 n8_gn8" />

            <route id="2to1" edges="gn2_n2 n2_c1 c1_c2 c2_j1 j1_n1 n1_gn1" />
            <route id="2to3" edges="gn2_n2 n2_c1 c1_c2 c2_j1 j1_a2 a2_a3 a3_j2 j2_f1 f1_f2 f2_n3 n3_gn3" />
            <route id="2to4" edges="gn2_n2 n2_c1 c1_c2 c2_j1 j1_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_h3 h3_n4 n4_gn4" />
            <route id="2to5" edges="gn2_n2 n2_c1 c1_c2 c2_j1 j1_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_a6 a6_a7 a7_j4 j4_n5 n5_gn5" />
            <route id="2to6" edges="gn2_n2 n2_c1 c1_c2 c2_j1 j1_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_a6 a6_a7 a7_j4 j4_n6 n6_gn6" />
            <route id="2to7" edges="gn2_n2 n2_c1 c1_c2 c2_j1 j1_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_g2 g2_n7 n7_gn7" />
            <route id="2to8" edges="gn2_n2 n2_c1 c1_c2 c2_j1 j1_c3 c3_n8 n8_gn8" />
            
            <route id="3to1" edges="gn3_n3 n3_e1 e1_b4 b4_b5 b5_b6 b6_j1 j1_n1 n1_gn1" />
            <route id="3to2" edges="gn3_n3 n3_e1 e1_b4 b4_b5 b5_b6 b6_d4 d4_d5 d5_n2 n2_gn2" />
            <route id="3to4" edges="gn3_n3 n3_e1 e1_j2 j2_a4 a4_a5 a5_j3 j3_h3 h3_n4 n4_gn4" />
            <route id="3to5" edges="gn3_n3 n3_e1 e1_j2 j2_a4 a4_a5 a5_j3 j3_a6 a6_a7 a7_j4 j4_n5 n5_gn5" />
            <route id="3to6" edges="gn3_n3 n3_e1 e1_j2 j2_a4 a4_a5 a5_j3 j3_a6 a6_a7 a7_j4 j4_n6 n6_gn6" />
            <route id="3to7" edges="gn3_n3 n3_e1 e1_j2 j2_a4 a4_a5 a5_g2 g2_n7 n7_gn7" />
            <route id="3to8" edges="gn3_n3 n3_e1 e1_b4 b4_b5 b5_b6 b6_j1 j1_c3 c3_n8 n8_gn8" />
            
            <route id="4to1" edges="gn4_n4 n4_g1 g1_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_j1 j1_n1 n1_gn1" />
            <route id="4to2" edges="gn4_n4 n4_g1 g1_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_d4 d4_d5 d5_n2 n2_gn2" />
            <route id="4to3" edges="gn4_n4 n4_g1 g1_b2 b2_b3 b3_f1 f1_f2 f2_n3 n3_gn3" />
            <route id="4to5" edges="gn4_n4 n4_g1 g1_j3 j3_a6 a6_a7 a7_j4 j4_n5 n5_gn5" />
            <route id="4to6" edges="gn4_n4 n4_g1 g1_j3 j3_a6 a6_a7 a7_j4 j4_n6 n6_gn6" />
            <route id="4to7" edges="gn4_n4 n4_g1 g1_j3 j3_g2 g2_n7 n7_gn7" />
            <route id="4to8" edges="gn4_n4 n4_g1 g1_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_j1 j1_c3 c3_n8 n8_gn8" />
            
            <route id="5to1" edges="gn5_n5 n5_j4 j4_b1 b1_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_j1 j1_n1 n1_gn1" />
            <route id="5to2" edges="gn5_n5 n5_j4 j4_b1 b1_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_d4 d4_d5 d5_n2 n2_gn2" />
            <route id="5to3" edges="gn5_n5 n5_j4 j4_b1 b1_j3 j3_b2 b2_b3 b3_f1 f1_f2 f2_n3 n3_gn3" />
            <route id="5to4" edges="gn5_n5 n5_j4 j4_b1 b1_j3 j3_h3 h3_n4 n4_gn4" />
            <route id="5to6" edges="gn5_n5 n5_j4 j4_n6 n6_gn6" />
            <route id="5to7" edges="gn5_n5 n5_j4 j4_b1 b1_j3 j3_g2 g2_n7 n7_gn7" />
            <route id="5to8" edges="gn5_n5 n5_j4 j4_b1 b1_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_j1 j1_c3 c3_n8 n8_gn8" />
            
            <route id="6to1" edges="gn6_n6 n6_j4 j4_b1 b1_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_j1 j1_n1 n1_gn1" />
            <route id="6to2" edges="gn6_n6 n6_j4 j4_b1 b1_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_d4 d4_d5 d5_n2 n2_gn2" />
            <route id="6to3" edges="gn6_n6 n6_j4 j4_b1 b1_j3 j3_b2 b2_b3 b3_f1 f1_f2 f2_n3 n3_gn3" />
            <route id="6to4" edges="gn6_n6 n6_j4 j4_b1 b1_j3 j3_h3 h3_n4 n4_gn4" />
            <route id="6to5" edges="gn6_n6 n6_j4 j4_n5 n5_gn5" />
            <route id="6to7" edges="gn6_n6 n6_j4 j4_b1 b1_j3 j3_g2 g2_n7 n7_gn7" />
            <route id="6to8" edges="gn6_n6 n6_j4 j4_b1 b1_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_j1 j1_c3 c3_n8 n8_gn8" />
            
            <route id="7to1" edges="gn7_n7 n7_h1 h1_h2 h2_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_j1 j1_n1 n1_gn1" />
            <route id="7to2" edges="gn7_n7 n7_h1 h1_h2 h2_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_d4 d4_d5 d5_n2 n2_gn2" />
            <route id="7to3" edges="gn7_n7 n7_h1 h1_h2 h2_j3 j3_b2 b2_b3 b3_f1 f1_f2 f2_n3 n3_gn3" />
            <route id="7to4" edges="gn7_n7 n7_h1 h1_h2 h2_j3 j3_h3 h3_n4 n4_gn4" />
            <route id="7to5" edges="gn7_n7 n7_h1 h1_h2 h2_a6 a6_a7 a7_j4 j4_n5 n5_gn5" />
            <route id="7to6" edges="gn7_n7 n7_h1 h1_h2 h2_a6 a6_a7 a7_j4 j4_n6 n6_gn6" />
            <route id="7to8" edges="gn7_n7 n7_h1 h1_h2 h2_j3 j3_b2 b2_b3 b3_j2 j2_b4 b4_b5 b5_b6 b6_j1 j1_c3 c3_n8 n8_gn8" />
            
            <route id="8to1" edges="gn8_n8 n8_d1 d1_d2 d2_d3 d3_j1 j1_n1 n1_gn1" />
            <route id="8to2" edges="gn8_n8 n8_d1 d1_d2 d2_d3 d3_j1 j1_d4 d4_d5 d5_n2 n2_gn2" />
            <route id="8to3" edges="gn8_n8 n8_d1 d1_d2 d2_d3 d3_a2 a2_a3 a3_j2 j2_f1 f1_f2 f2_n3 n3_gn3" />
            <route id="8to4" edges="gn8_n8 n8_d1 d1_d2 d2_d3 d3_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_h3 h3_n4 n4_gn4" />
            <route id="8to5" edges="gn8_n8 n8_d1 d1_d2 d2_d3 d3_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_a6 a6_a7 a7_j4 j4_n5 n5_gn5" />
            <route id="8to6" edges="gn8_n8 n8_d1 d1_d2 d2_d3 d3_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_j3 j3_a6 a6_a7 a7_j4 j4_n6 n6_gn6" />
            <route id="8to7" edges="gn8_n8 n8_d1 d1_d2 d2_d3 d3_a2 a2_a3 a3_j2 j2_a4 a4_a5 a5_g2 g2_n7 n7_gn7" />
            """, file=routes)

        data_count = {name: 0 for name in column_names}
        vehNum = 0
        for time in range(1, 3600):
            for ODname in column_names:
                if data_count[ODname] < (OD.loc[Num, ODname] / 3600 * time):
                    print(f'    <vehicle id="veh_%i" type="car" route="{ODname}" depart="%i" />' % (vehNum, time),
                          file=routes)
                    vehNum += 1
                    data_count[ODname] += 1
        print("</routes>", file=routes)
        print(Num, " route file is complete")


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1
    traci.close()
    sys.stdout.flush()


def generate_phases(data, Num):
    TL = data.loc[Num]


    with open(('data' + os.sep + 'fyp' + str(Num) + '.add.xml'), 'w') as phases:
        print(
            """
            <additional>
            <tlLogic id="j1" programID="j1_program" offset="%i" type="static">
            <phase duration="%i"  state="rrrGGrrrrGGGr"/>
            <phase duration="4"  state="rrrGGrrrryyyr"/>
            <phase duration="%i"  state="rrrGGGrrrrrrr"/>
            <phase duration="4"  state="rrryyyrrrrrrr"/>
            <phase duration="%i"  state="rrrrrrrrrGGGG"/>
            <phase duration="4"  state="rrrrrrrrryyyy"/>
            <phase duration="%i"  state="GGGrrrrrrrrrr"/>
            <phase duration="4"  state="GGyrrrrrrrrrr"/>
            <phase duration="%i"  state="GGrrrrGGrrrrr"/>
            <phase duration="4"  state="yyrrrrGGrrrrr"/>
            <phase duration="%i"  state="rrrrrrGGGrrrr"/>
            <phase duration="4"  state="rrrrrryyyrrrr"/>
            </tlLogic>
            """ % (TL[19], TL[0], TL[1], TL[2], TL[3], TL[4], TL[5]),
            """
            <tlLogic id="j2" programID="j2_program" offset="%i" type="static">    
            <phase duration="%i"  state="rrGGGGr"/>
            <phase duration="4"  state="rryyGGr"/>
            <phase duration="%i"  state="rrrrGGG"/>
            <phase duration="4"  state="rrrryyy"/>
            <phase duration="%i"  state="GGrrrrr"/>
            <phase duration="4"  state="yyrrrrr"/>
            <phase duration="%i"  state="rrrrGGG"/>
            <phase duration="4"  state="rrrrGGy"/>
            </tlLogic>
            """ % (TL[20], TL[6], TL[7], TL[8], TL[9]),
            """
            <tlLogic id="j3" programID="j3_program" offset="%i" type="static">     
            <phase duration="%i"  state="rrrGGGrrrrGGrr"/>
            <phase duration="4"  state="rrryyyrrrrGGrr"/>
            <phase duration="%i"  state="rrrrrrrrrrGGGG"/>
            <phase duration="4"  state="rrrrrrrrrryyyy"/>
            <phase duration="%i"  state="rrrGGGGrrrrrrr"/>
            <phase duration="4"  state="rrrGyyyrrrrrrr"/>
            <phase duration="%i"  state="rrGGrrrrrGrrrr"/>
            <phase duration="4"  state="rryyrrrrrGrrrr"/>
            <phase duration="%i"  state="rrrrrrrGGGrrrr"/>
            <phase duration="4"  state="rrrrrrryyyrrrr"/>
            <phase duration="%i"  state="GGGGrrrrrrrrrr"/>
            <phase duration="4"  state="yyyGrrrrrrrrrr"/>
            </tlLogic>
            """ % (TL[21], TL[10], TL[11], TL[12], TL[13], TL[14], TL[15]),
            """
            <tlLogic id="j4" programID="j4_program" offset="%i" type="static">    
            <phase duration="%i"  state="rrGGGGGr"/>
            <phase duration="4"  state="rryyyGGr"/>
            <phase duration="%i"  state="GrrrrGGG"/>
            <phase duration="4"  state="Grrrryyy"/>
            <phase duration="%i"  state="GGGrrrrr"/>
            <phase duration="4"  state="yyGrrrrr"/>
            </tlLogic>
            </additional>
            """ % (TL[22], TL[16], TL[17], TL[18]), file=phases)


def create_sumocfg(N):
    with open('data' + os.sep + 'net' + str(N) + '.sumocfg', 'w') as cfg:
        print(f"""<configuration>
    <input>
        <net-file value="final_net.net.xml"/>
        <route-files value="fyp{N}.rou.xml"/>
        <additional-files value="fyp{N}.add.xml"/>
    </input>
    <time>
        <begin value="0"/>
    </time>
    <report>
        <verbose value="true"/>
        <no-step-log value="true"/>
    </report>
</configuration>""", file=cfg)


if __name__=="__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    for data_num in range(480):
        traci.start([sumoBinary, "-c", "data/net" + str(data_num) + ".sumocfg",
                     "--tripinfo-output", "tripinfo" + str(data_num) + ".xml"])
        run()



# A code to generate route files
"""if __name__=="__main__":
    data = open_data('data_input.csv')
    for step in range(data.shape[0]):
        generate_routefile(data, step)"""


# A code to generate phase times
"""if __name__=="__main__":
    TLtiming = pd.read_csv("data" + os.sep + "tl_timing.csv", usecols=cols)
    for i in range(480):
        generate_phases(TLtiming, i)"""

# A code to generate sumocfg file
"""if __name__=="__main__":
    for i in range(480):
        create_sumocfg(i)
        print(i, 'FINISHED')
"""
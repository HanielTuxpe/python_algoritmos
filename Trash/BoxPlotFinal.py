from DifEvo_Bound import main
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import Boundexp1 as exp1
import Randomexp1 as exp2
import Reflexexp1 as exp3

class SphereBoxPlot:
    exp1Result= exp1.main() 
    exp2Result= exp2.main()

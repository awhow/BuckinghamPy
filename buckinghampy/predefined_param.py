
# List of dimensions and associated names.
knownParamDict = {
'mass': [1],                   # Basic types
'length': [0,1],
'time': [0,0,1],
'temperature': [0,0,0,1],
'area': [0,2],                 # Geometry
'volumne': [0,3],
'secondMomentOfArea': [0,4],
'velocity': [0,1,-1],          # Kinematics
'acceleration': [0,1,-2],
'angle': [0],
'angularVelocity': [0,0,-1],
'volumneFlowRate': [0,3,-1],
'massFlowRate': [1,0,-1],
'force': [1,1,-2],             # Dynamics
'torque': [1,2,-2],
'moment': [1,2,-2],
'energy': [1,2,-2],
'power': [1,2,-3],
'pressure': [1,-1,-2],
'stress': [1,-1,-2],
'density': [1,-3],             # Fluid Properties
'viscosity': [1,-1,-1],
'kinematicViscosity': [0,2,-1],
'conductivity': [1,1,-3,-1],
'specificHeat': [0,2,-2,-1]
}

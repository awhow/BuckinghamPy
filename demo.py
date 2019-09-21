import buckinghampy as bp

print("Running...")
print("Simple pendululm example")

# Create parameters
theta = bp.Param('theta')
theta0  = bp.Param('theta0')
mass = bp.Param('m', ptype='mass')
length = bp.Param('l', ptype='length')
gravity = bp.Param('g', ptype='acceleration')
time = bp.Param('t', ptype='time')

# Create list of parameters
paramList = [theta, theta0, mass, length, gravity, time]
repeatingList = [mass, length, time]

# Run nondimensionalization process
pgl = bp.run(paramList, repeatingList)
bp.pprint(pgl)



print("")
print("Pipe flow pressure drop")

# Create parameters
DeltaP = bp.Param('DeltaP', dim=[1,-2,-2])
diameter = bp.Param('D', ptype='length')
relruf = bp.Param('eps', ptype='length')
density = bp.Param('rho', ptype='density')
viscosity = bp.Param('mu', ptype='viscosity')
velocity = bp.Param('V', ptype='velocity')

# Create list of parameters
paramList = [DeltaP, diameter, relruf, density, viscosity, velocity]
repeatingList = [diameter, density, velocity]

# Run nondimensionalization process
pgl = bp.run(paramList, repeatingList)
bp.pprint(pgl)



print("")
print("Lift on a Wing")

# Create parameters
lift = bp.Param('FL', ptype='force')
velocity = bp.Param('V', ptype='velocity')
cord = bp.Param('Lc', ptype='length')
density = bp.Param('rho', ptype='density')
viscosity = bp.Param('mu', ptype='viscosity')
soundspeed = bp.Param('c', ptype='velocity')
attack = bp.Param('alpha', ptype='angle')

# Create list of parameters
paramList = [lift, velocity, cord, density, viscosity, soundspeed, attack]

# Run nondimensionalization process
pgl = bp.run(paramList, depParam=lift)
bp.pprint(pgl)



print("")
print("Tip Deflection of Cantilever Beam")

# Create parameters
deflection = bp.Param('delta', ptype='length')
load = bp.Param('W', ptype='force')
length = bp.Param('L', ptype='length')
secMomArea = bp.Param('I', ptype='secondMomentOfArea')
modulus = bp.Param('E', dim=[1,-1,-2])

# Create list of parameters
paramList = [deflection, load, length, secMomArea, modulus]

# Run nondimensionalization process
pgl = bp.run(paramList, depParam=deflection)
bp.pprint(pgl)



print("")
print('done.')


import buckinghampy as bp

print("Running...")
print("Simple pendululm example")

# Create parameters
theta = bp.param('theta')
theta0  = bp.param('theta0')
mass = bp.param('m', ptype='mass')
length = bp.param('l', ptype='length')
gravity = bp.param('g', ptype='acceleration')
time = bp.param('t', ptype='time')

# Create list of parameters
paramList = [theta, theta0, mass, length, gravity, time]
repeatingList = [mass, length, time]

# Run nondimensionalization process
pgl = bp.run(paramList, repeatingList)
bp.pprint(pgl)



print("")
print("Pipe flow pressure drop")

# Create parameters
DeltaP = bp.param('DeltaP', dim=[1,-2,-2])
diameter = bp.param('D', ptype='length')
relruf = bp.param('eps', ptype='length')
density = bp.param('rho', ptype='density')
viscosity = bp.param('mu', ptype='viscosity')
velocity = bp.param('V', ptype='velocity')

# Create list of parameters
paramList = [DeltaP, diameter, relruf, density, viscosity, velocity]
repeatingList = [diameter, density, velocity]

# Run nondimensionalization process
pgl = bp.run(paramList, repeatingList)
bp.pprint(pgl)

print("")
print('done.')



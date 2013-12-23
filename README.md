# BuckinghamPy

Taking the leg work out of dimensional analysis.

## What to do

Import the module as buckinghampy.

     import buckinghampy as bp

Create some parameters. For instance, I can create a parameter with

     diameter = bp.param('D', dim=[0,1])

Here _D_ is the parameter's symbol and _dim_ is the dimension of the parameter. The dimension array is represented by a vector where each index location corresponds to a base dimension. 

     dimensional vector: [ M L t T N I J ]
     1 Mass (ex. kilogram, k)
     2 Length (ex. meter, m)
     3 Time (ex. second, s)
     4 Temperature (ex. Kelvin, K)
     5 Quantity (ex. moles, mol)
     6 Current (ex. ampere, A)
     7 Luminous intensity (ex. candela, cd)

For convience, common parameter archetypes are available using _ptype_. For example, I could have defined the diameter as

     diameter = bp.param('D', ptype='length')

After a number of parameters have been created, join them in a list.

     paramList = [diameter, density, viscosity, velocity]

Then run the dimensional analysis to get the resulting list of Pi-Groups and then print the list.

     pgl = bp.run(paramList)
     bp.pprint(pgl)

## Example: Pipe flow pressure drop

A common early example for dimensional analysis: find the important non-dimensional parameters for pressure drop due to flow in a pipe.

     # Important parameters
     DeltaP = bp.param('DeltaP', dim=[1,-2,-2])
     diameter = bp.param('D', ptype='length')
     relruf = bp.param('eps', ptype='length')
     density = bp.param('rho', ptype='density')
     viscosity = bp.param('mu', ptype='viscosity')
     velocity = bp.param('V', ptype='velocity')

     # Create list of parameters
     paramList = [DeltaP, diameter, relruf, density, viscosity, velocity]
     repeatingList = [diameter, density, velocity]

Here I am specifying the repeating variables to use, but I could not specify and let the module figure it out. Additionally, I could tell pass the option argument _depParam=DeltaP_ to the module that _DeltaP_ is the dependent parameter and should not be included in the repeating variable list.

     # Run nondimensionalization process
     pgl = bp.run(paramList, repeatingList)
     bp.pprint(pgl)

The output of _bp.pprint_ is

     Pi-Group 1:  (D) (DeltaP) (rho)^-1 (V)^-2 
     Pi-Group 2:  (D) (eps)^-1 
     Pi-Group 3:  (D) (V) (rho) (mu)^-1 

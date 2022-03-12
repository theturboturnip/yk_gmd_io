"""


Noise Utilities (mathutils.noise)
*********************************

The Blender noise module

:func:`cell`

:func:`cell_vector`

:func:`fractal`

:func:`hetero_terrain`

:func:`hybrid_multi_fractal`

:func:`multi_fractal`

:func:`noise`

:func:`noise_vector`

:func:`random`

:func:`random_unit_vector`

:func:`random_vector`

:func:`ridged_multi_fractal`

:func:`seed_set`

:func:`turbulence`

:func:`turbulence_vector`

:func:`variable_lacunarity`

:func:`voronoi`

"""

import typing

import mathutils

def cell(position: mathutils.Vector) -> float:

  """

  Returns cell noise value at the specified position.

  """

  ...

def cell_vector(position: mathutils.Vector) -> mathutils.Vector:

  """

  Returns cell noise vector at the specified position.

  """

  ...

def fractal(position: mathutils.Vector, H: float, lacunarity: float, octaves: int, noise_basis: str = 'PERLIN_ORIGINAL') -> float:

  """

  Returns the fractal Brownian motion (fBm) noise value from the noise basis at the specified position.

  """

  ...

def hetero_terrain(position: mathutils.Vector, H: float, lacunarity: float, octaves: int, offset: float, noise_basis: str = 'PERLIN_ORIGINAL') -> float:

  """

  Returns the heterogeneous terrain value from the noise basis at the specified position.

  """

  ...

def hybrid_multi_fractal(position: mathutils.Vector, H: float, lacunarity: float, octaves: int, offset: float, gain: float, noise_basis: str = 'PERLIN_ORIGINAL') -> float:

  """

  Returns hybrid multifractal value from the noise basis at the specified position.

  """

  ...

def multi_fractal(position: mathutils.Vector, H: float, lacunarity: float, octaves: int, noise_basis: str = 'PERLIN_ORIGINAL') -> float:

  """

  Returns multifractal noise value from the noise basis at the specified position.

  """

  ...

def noise(position: mathutils.Vector, noise_basis: str = 'PERLIN_ORIGINAL') -> float:

  """

  Returns noise value from the noise basis at the position specified.

  """

  ...

def noise_vector(position: mathutils.Vector, noise_basis: str = 'PERLIN_ORIGINAL') -> mathutils.Vector:

  """

  Returns the noise vector from the noise basis at the specified position.

  """

  ...

def random() -> float:

  """

  Returns a random number in the range [0, 1).

  """

  ...

def random_unit_vector(size: int = 3) -> mathutils.Vector:

  """

  Returns a unit vector with random entries.

  """

  ...

def random_vector(size: int = 3) -> mathutils.Vector:

  """

  Returns a vector with random entries in the range (-1, 1).

  """

  ...

def ridged_multi_fractal(position: mathutils.Vector, H: float, lacunarity: float, octaves: int, offset: float, gain: float, noise_basis: str = 'PERLIN_ORIGINAL') -> float:

  """

  Returns ridged multifractal value from the noise basis at the specified position.

  """

  ...

def seed_set(seed: int) -> None:

  """

  Sets the random seed used for random_unit_vector, and random.

  """

  ...

def turbulence(position: mathutils.Vector, octaves: int, hard: bool, noise_basis: str = 'PERLIN_ORIGINAL', amplitude_scale: float = 0.5, frequency_scale: float = 2.0) -> float:

  """

  Returns the turbulence value from the noise basis at the specified position.

  """

  ...

def turbulence_vector(position: mathutils.Vector, octaves: int, hard: bool, noise_basis: str = 'PERLIN_ORIGINAL', amplitude_scale: float = 0.5, frequency_scale: float = 2.0) -> mathutils.Vector:

  """

  Returns the turbulence vector from the noise basis at the specified position.

  """

  ...

def variable_lacunarity(position: mathutils.Vector, distortion: float, noise_type1: str = 'PERLIN_ORIGINAL', noise_type2: str = 'PERLIN_ORIGINAL') -> float:

  """

  Returns variable lacunarity noise value, a distorted variety of noise, from noise type 1 distorted by noise type 2 at the specified position.

  """

  ...

def voronoi(position: mathutils.Vector, distance_metric: str = 'DISTANCE', exponent: float = 2.5) -> typing.List[typing.Any]:

  """

  Returns a list of distances to the four closest features and their locations.

  """

  ...

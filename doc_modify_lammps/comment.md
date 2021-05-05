# Comments to lammps

## system
Assume a system which exsits in an external field,
thus the total linear momentum of this system is not conserved and its center of mass should undergo a random walk.

Lammps documentation [link](https://lammps.sandia.gov/doc/fix_nh.html)

> This implementation has been shown to conserve linear momentum up to machine precision under NVT dynamics. Under NPT dynamics, for a system with zero initial total linear momentum, the total momentum fluctuates close to zero. It may occasionally undergo brief excursions to non-negligible values, before returning close to zero. Over long simulations, this has the effect of causing the center-of-mass to undergo a slow random walk. This can be mitigated by resetting the momentum at infrequent intervals using the fix momentum command.

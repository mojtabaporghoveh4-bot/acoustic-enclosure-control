function v = CONS(x,y,z,CavityDim)
% CONS  Geometric constraint-violation measure for a secondary source position.
%
% RECONSTRUCTED FILE. The original CONS.m was missing from the author's archive.
% It is used by PSO_2Speaker_Pressure_Min*.m and Kuri_Murales_Cost_PSO.m only to
% report (or penalise) whether an optimiser-proposed source sits inside the
% cavity box [0,Lx] x [0,Ly] x [0,Lz].
%
% This reconstruction returns 0 when the point is inside the box and the total
% Euclidean overshoot distance when it is outside. The PSO search bounds already
% clamp positions to the box, so in the archived runs this evaluates to 0; the
% exact original penalty shape could not be recovered.
%
%   x,y,z     : candidate source coordinates [m]
%   CavityDim : struct with fields X, Y, Z (cavity dimensions [m])
%   v         : >= 0, zero iff the point lies inside the cavity

lo = [0 0 0];
hi = [CavityDim.X, CavityDim.Y, CavityDim.Z];
p  = [x y z];
over = max(p - hi, 0) + max(lo - p, 0);
v = norm(over);
end

function yy = acc_mode_ne(x,y,z,Lx,Ly,Lz,n)
% acc_mode_ne  Rigid-walled cavity acoustic mode shape(s) at a point.
%
% RECONSTRUCTED FILE. The original acc_mode_ne.m was missing from the author's
% archive. It is called by Accffs_opt_TwoSpkr.m with a single (x,y,z) point.
% This reconstruction is identical in form to acc_mode_ne_sen.m (which *was*
% archived) and has been checked to reproduce the fully-coupled pressure stored
% in the WeightedSensorWithForce_*.mat result files to machine precision.
%
%   n  : (M x 3) matrix of cavity modal indices [n1 n2 n3]
%   x,y,z : point coordinates (scalars, or column vectors of P points)
%   Lx,Ly,Lz : cavity dimensions [m]
%   yy : (M x P) mode-shape values, with the sqrt(2)^(#non-zero indices) norm.

x = x(:); y = y(:); z = z(:);
N  = VNonZeros(n);          % number of non-zero indices per mode
er = sqrt(2);
yy = zeros(size(n,1), numel(x));
for i = 1:numel(x)
    yy(:,i) = ( er.^N ) ...
        .* cos( x(i) .* (pi*n(:,1))./Lx ) ...
        .* cos( y(i) .* (pi*n(:,2))./Ly ) ...
        .* cos( z(i) .* (pi*n(:,3))./Lz );
end
end

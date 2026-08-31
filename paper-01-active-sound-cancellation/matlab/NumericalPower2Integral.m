function y2=NumericalPower2Integral(ACOEF,x,y,z,Lx,Ly,Lz,n,dv)

% This function calculates the absolute value of the pressure inside the
% region defined by x,y and z meshed
% x is the meshed x-wise dimension of the region
% y and z are the same for y and z wise mesh of the region
% Lx Ly and Lz are the dimension of the cavity
% n is the mode indices of the cavity
% dv is the volume element of integration





outsize=size(x);
N=VNonZeros(n);	    % number of nonzero indices of a mode number
AMode=size(n,1);    % number of acoustic modes
er=sqrt(2);
y2=zeros(outsize);


for i=1:AMode
    
    % each mode-shape is evaluated in all points of the region
    
    y3=(ACOEF(i))*(( er.^N(i)  ).*( cos(  x.* ( pi*n(i,1) )./Lx ) ).* cos(  y.* ( pi*n(i,2) )./Ly ).*( cos(  z.* ( pi*n(i,3) )./Lz ) )); 
    
    % Colecting sum of all modes
    
    y2=y2+y3;
        
end

% absolute value of the sum pressure-modes
y2=(abs(y2)).^2;

% the integration
y2=dv*sum(y2(:));


end
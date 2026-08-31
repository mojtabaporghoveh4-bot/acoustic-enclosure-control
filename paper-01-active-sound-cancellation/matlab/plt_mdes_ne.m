function y=plt_mdes_ne(x,y,Lx,Ly,m)
% m is the mode index
y=2*( sin(  x* ( pi*m(:,1) )/Lx ) )  .* sin(  y* ( pi*m(:,2) )/Ly ); 

end
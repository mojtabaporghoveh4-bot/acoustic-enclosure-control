function yy=acc_mode_ne_sen(x,y,z,Lx,Ly,Lz,n)
% This function calculates the accoustic mode index given in Matrix
yy=zeros(size(n,1),size(x,1));
N=VNonZeros(n);
er=sqrt(2);

for i=1:size(x,1)
yy(:,i)=( er.^N  ).*( cos(  x(i).* ( pi*n(:,1) )./Lx ) ).* cos(  y(i).* ( pi*n(:,2) )./Ly ).*( cos(  z(i).* ( pi*n(:,3) )./Lz ) ); 
end

end
function acoef=Accffs_opt_TwoSpkr(Q,Force,w,plate,cavity,C)
% this function gives the acoustic coefficient of the cavity modes 
% Q(1:3) is the position of the 1st secondary sound source(s) 
% Q(4) is the amplitude of the 1st secondary sound source
% Q(5:7) is the position of the 2nd secondary sound source(s)
% Q(8) is the amplitude of the 2nd secondary sound source
% plate and cavity are structures containig properties of the system (size,mode number and index . . .)
% The system is considered as fully coupled
% Force is structure with Force.Amp and Force.Location

Force_Amp=Force.Amp;
Force_location=Force.Location;

% Size
Lx=cavity.dim.x;
Ly=cavity.dim.y;
Lz=cavity.dim.z;


% Generalization of the External Force

g=zeros(plate.mode,1);
B=zeros(plate.mode);

for i=1:plate.mode
  
   g(i)=Force_Amp.* plt_mdes_ne(Force_location(1),Force_location(2),Lx,Ly,plate.ModeIndex(i,:)) ;
   
   B(i,i)=1i*w/(  ( plate.radfreq(i) )^2-w^2+2*1i*plate.damping*w*plate.radfreq(i) ) ;
end



% External Sound Source Parameters: The optimization Parameters


% Generating the generalized accoustic source mode shapes
A=zeros(cavity.mode);
q=zeros(cavity.mode,1);

    for i=1:cavity.mode
        
       q(i,1)=Q(4).*acc_mode_ne(Q(1),Q(2),Q(3),Lx,Ly,Lz,cavity.ModeIndex(i,:))...
           +Q(8).*acc_mode_ne(Q(5),Q(6),Q(7),Lx,Ly,Lz,cavity.ModeIndex(i,:));
       
       A(i,i)= 1i*w/( (cavity.radfreq(i))^2-w^2+2*1i*cavity.damping*w*cavity.radfreq(i) ); 
    end
A(1,1)=1/(cavity.TimeConstant^-1+1i*w);

%% Part III The Solution %%

Za=(cavity.density*cavity.sndspeed^2/cavity.volume)*A;
Ys=B/(plate.density*plate.thickness*plate.area);

%% Fully Coupled Soulution  

 acoef=(eye(cavity.mode)+ Za*C*Ys*C' ) \ ( Za*(q+C*Ys*g) );   % Coefficients of the Cavity Modes
 
 


end
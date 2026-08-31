function pressure_f=CavityPressureSens(cavity,plate,Force,Q,C,w,X)

% this function is the fast version of fully coupled system of vehicle body
% and accoustic environment of the domain.
% Force contains the force amplitude and location,
% w is the frequency of intereset (excitation)
% X is the position of the interested point(s)
% Force contains the Force Amplitude and Force Position of the File
% Flexible Plate Properties are in the "plate" variable
% Cavity properties are in the "cavity" variable
% C is the coupling Matrix


% External Force Properties

 % The source has been considered frequency dependent with fixed amplitude
% Generalization of the External Force
g=zeros(plate.mode,1);
B=zeros(plate.mode);

for i=1:plate.mode
  
   g(i)=Force.Amp.* plt_mdes_ne(Force.Location(1),Force.Location(2),plate.dim.x,plate.dim.y,plate.ModeIndex(i,:)) ;
   
   B(i,i)=1i*w/(  ( plate.radfreq(i) )^2-w^2+2*1i*plate.damping*w*plate.radfreq(i) ) ;
end




%% External Sound Source Parameters: The optimization Parameters
% Generating the generalized accoustic source mode shapes
A=zeros(cavity.mode);
q=zeros(cavity.mode,1);

    for i=1:cavity.mode
        
       q(i,1)=Q(4).*acc_mode_ne_sen(Q(1),Q(2),Q(3),cavity.dim.x,cavity.dim.y,cavity.dim.z,cavity.ModeIndex(i,:))...
           +Q(8).*acc_mode_ne_sen(Q(5),Q(6),Q(7),cavity.dim.x,cavity.dim.y,cavity.dim.z,cavity.ModeIndex(i,:));
       
       A(i,i)= 1i*w/( (cavity.radfreq(i))^2-w^2+2*1i*cavity.damping*w*cavity.radfreq(i) ); 
    end
A(1,1)=1/(cavity.TimeConstant^-1+1i*w);

%% Part III The Solution %%

Za=(cavity.density*cavity.sndspeed^2/cavity.volume)*A;
Ys=B/(plate.density*plate.thickness*plate.area);



%% Fully Coupled Soulution  

 a=(eye(cavity.mode)+ Za*C*Ys*C' ) \ ( Za*(q+C*Ys*g) );   % Coefficients of the Cavity Modes

 

pressure_f=a.' * acc_mode_ne_sen(X(:,1),X(:,2),X(:,3),cavity.dim.x,cavity.dim.y,cavity.dim.z,cavity.ModeIndex);

% a_weak= Za*(q+C*Ys*g);
% pressure_w=a_weak.' *acc_mode_ne(X(1),X(2),X(3),cavity.dim.x,cavity.dim.y,cavity.dim.z,cavity.ModeIndex);   
%     
end
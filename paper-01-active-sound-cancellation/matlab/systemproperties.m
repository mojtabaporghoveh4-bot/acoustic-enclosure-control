function [plate,cavity,C]=systemproperties(dimension,MODES)
% Size of the Cavity
Lx=dimension.x;
Ly=dimension.y;
Lz=dimension.z;

% Number of modes
plate.mode=MODES.PLT;         % Number of plate modes
cavity.mode=MODES.AC;         % Number of cavity modes

% Flexible Plate Properties


plate.density=2770;     % [Kg/m^3] density of flexible plate
plate.poisson=0.33;     % Poisson ratio
plate.damping=0.01;     % Damping ratio of the plate
plate.area=Lx*Ly;       % [m^2] Area of the flexible plate
plate.thickness=5e-03;  % [m] thickness of the plate
plate.young=71e9;       % Young Modolus of the plate
plate.bending=(plate.young*plate.thickness^3)/(12*(1-plate.poisson^2));
plate.dim.x=Lx;     plate.dim.y=Ly;
[plate.radfreq,plate.ModeIndex]=plate_freq(plate);  % Mode indexes and natural frequencies


% Cavity properties

cavity.volume=Lx*Ly*Lz;
cavity.density=1.21;
cavity.sndspeed=340;        % sound speed in the domain
cavity.damping=0.01;        % damping ratio of the cavity
cavity.dim.x=Lx;cavity.dim.y=Ly;cavity.dim.z=Lz;
cavity.TimeConstant=0.2;    % Time Constant of the first Accoustic Mode
% cavity natural frequencies and modal indexes
[cavity.radfreq,cavity.ModeIndex]=cavity_freq(cavity);      % Mode indexes and natural frequencies

% Findig Coupling terms
C=zeros(cavity.mode,plate.mode);
    for j=1:cavity.mode
       for i=1:plate.mode

        C(j,i)=CplFast(plate,cavity,j,i);
       end
    end
    


end


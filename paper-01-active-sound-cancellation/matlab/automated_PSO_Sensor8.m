
% number of Microphones 
Mic_num=8;  

% Number of speakers
Spk_NUM=2;
Q=zeros(1,Spk_NUM*4);

% cavity size 
dimension.x=2.5; % X dimensio in [m] in meter
dimension.y=1.3;
dimension.z=1.4;

% External Force definition

%






%Force.Amp=800;   % Amplitute of the External force [N]
Force.Location=[13*dimension.x/30,dimension.y/2,dimension.z];  % Location of the imposed force

% number of modes and loading properties

MODES.AC=70;     % cavity modes
MODES.PLT=50;    % plate modes

[plate,cavity,C]=systemproperties(dimension,MODES);


% cavity size 
CavityDim.X=dimension.x; % X dimensio in [m] in meter
CavityDim.Y=dimension.y;
CavityDim.Z=dimension.z;

 % Maximum weight of each Microphone
MaxW=100;       

%opt properties

opt.Iter=500;
opt.nvar=Mic_num;
opt.Npop=30;


opt.min=zeros(1,opt.nvar);
opt.max=repmat(MaxW,1,Mic_num);

%% Microphone Positions
mic(1,:)=[0, 0, 1].*[dimension.x, dimension.y, dimension.z]; % Left corner
mic(2,:)=[0, 1, 1].*[dimension.x, dimension.y, dimension.z]; % Right corner
mic(3,:)=[1/3, 1/2, 1].*[dimension.x, dimension.y, dimension.z]; % on the roof in line with the headrest position
mic(4,:)=[0, 1/4, 3/5].*[dimension.x, dimension.y, dimension.z]; % Headrest position
mic(5,:)=[1/3, 1/4, 1].*[dimension.x, dimension.y, dimension.z]; % Headrest position
mic(6,:)=[1/3, 0, 3/5].*[dimension.x, dimension.y, dimension.z];
mic(7,:)=[1/3, 1, 3/5].*[dimension.x, dimension.y, dimension.z];
mic(8,:)=[0, 1/2, 1/2].*[dimension.x, dimension.y, dimension.z];


%% Headrest Position
Pinterest=[1/3, 1/4, 3/5].*[dimension.x, dimension.y, dimension.z];

% numerical integration precision

% precision.X=120;
% precision.Y=80;
% precision.Z=60;
% 
% 
% % Region size
% 
% RegionDim.X=[CavityDim.X/8,CavityDim.X/6];
% RegionDim.Y=[CavityDim.Y/8,CavityDim.Y/3];
% RegionDim.Z=[CavityDim.Z/8,CavityDim.Z/6];


% % Region Mesh for integration
% 
% Xreg=linspace(RegionDim.X(1),RegionDim.X(2),precision.X);
% Yreg=linspace(RegionDim.Y(1),RegionDim.Y(2),precision.Y);
% Zreg=linspace(RegionDim.Z(1),RegionDim.Z(2),precision.Z);
% 
% [Xmesh,Ymesh,Zmesh]=meshgrid(Xreg,Yreg,Zreg);
% 
% dv=(Xreg(2)-Xreg(1))*(Yreg(2)-Yreg(1))*(Zreg(2)-Zreg(1));   % volume element
% 

% range of frequency 
Ffinal=400;                  % final frequency of the simulation
fs=100;                       % number of samples 
fbegin=20;
f=linspace(fbegin,Ffinal,fs);     % range of frequency in [Hz] 



% getting the cost function ready

w=2*pi*f;

Cost=@(weight,W) abs( mean(weight .* CavityPressureSens(cavity,plate,Force,Q,C,W,mic) ) -(CavityPressureSens(cavity,plate,Force,Q,C,W,Pinterest)  ));
% Aq=@(X,W) Accffs_opt_TwoSpkr(X,Force,W,plate,cavity,C);   % Acoustic coeficient as a function of position and strength of the secondary sound source


% cost function of the problem

% The optimization procedure using PSO algorithm

% Preallocating for positions,Absulute Pressure Integral and Violation

Wbest=zeros(fs,opt.nvar);  % weights of each microphone in each strategy
MinDifSensd=zeros(fs,1);
Cost_no=zeros(1,fs);
EstimatedPres=zeros(fs,1);
ActualPres=zeros(fs,1);
disp(['The optimization with 8 sensors and ' num2str(Force.Amp) 'N engine force'])
for i = 1:fs
   
    disp(['The optimization for the ' num2str(i) 'th frequency (' num2str(f(i)) ' Hz) is started'])
    % The cost function changes as the frequency changes
    Cost_free=@(X) Cost(X,w(i));
tic
    % The PSO optimization 
    [MinDifSensd(i),Wbest(i,:)]=Best_PSO_COMPLETED(Cost_free,opt);
toc    
    EstimatedPres(i)=abs(mean(Wbest(i,:) .* CavityPressureSens(cavity,plate,Force,Q,C,w(i),mic) )); 
    ActualPres(i)=abs(CavityPressureSens(cavity,plate,Force,Q,C,w(i),Pinterest));
end

save(['WeightedSensorWithForce L' num2str(Force.Amp) ' ' ])




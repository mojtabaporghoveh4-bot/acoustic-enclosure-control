clear
clc
close all

% number of Speakers
Spk_num=2;  

% cavity size 
dimension.x=2.5; % X dimensio in [m] in meter
dimension.y=1.3;
dimension.z=1.4;

% External Force definition

Force.Amp=1000;   % Amplitute of the External force [N]
Force.Location=[13*dimension.x/30,dimension.y/2,dimension.z];  % Location of the imposed force

% number of modes and loading properties

MODES.AC=70;     % cavity modes
MODES.PLT=50;    % plate modes

[plate,cavity,C]=systemproperties(dimension,MODES);


% cavity size 
CavityDim.X=dimension.x; % X dimensio in [m] in meter
CavityDim.Y=dimension.y;
CavityDim.Z=dimension.z;

 % Maximum volume velocity of the secondary sound source
MaxQ=10;       

%opt properties

opt.Iter=1000;
opt.nvar=8;
opt.Npop=30;
maxval=[cavity.dim.x,cavity.dim.y,cavity.dim.z,MaxQ];

opt.min=zeros(1,opt.nvar);
opt.max=repmat(maxval,1,Spk_num);

% numerical integration precision

precision.X=120;
precision.Y=80;
precision.Z=60;


% Region size

RegionDim.X=[CavityDim.X/8,CavityDim.X/6];
RegionDim.Y=[CavityDim.Y/8,CavityDim.Y/3];
RegionDim.Z=[CavityDim.Z/8,CavityDim.Z/6];


% Region Mesh for integration

Xreg=linspace(RegionDim.X(1),RegionDim.X(2),precision.X);
Yreg=linspace(RegionDim.Y(1),RegionDim.Y(2),precision.Y);
Zreg=linspace(RegionDim.Z(1),RegionDim.Z(2),precision.Z);

[Xmesh,Ymesh,Zmesh]=meshgrid(Xreg,Yreg,Zreg);

dv=(Xreg(2)-Xreg(1))*(Yreg(2)-Yreg(1))*(Zreg(2)-Zreg(1));   % volume element


% range of frequency 
Ffinal=400;                  % final frequency of the simulation
fs=20;                       % number of samples (array strategy)
fbegin=20;
f=linspace(fbegin,Ffinal,fs);     % range of frequency in [Hz] 



% getting the cost function ready

w=2*pi*f;

Aq=@(X,W) Accffs_opt_TwoSpkr(X,Force,W,plate,cavity,C);   % Acoustic coeficient as a function of position and strength of the secondary sound source


% cost function of the problem

% The optimization procedure using PSO algorithm

% Preallocating for positions,Absulute Pressure Integral and Violation

Qbest=zeros(fs,opt.nvar);  % [Qbest(1),Qbest(2),Qbest(3),Qamp] in each strategy
BestIntPr=zeros(fs,1);
violation_opt=zeros(fs,2);
Cost_no=zeros(1,fs);
disp(['The optimization with 2 speakers started for ' num2str(Force.Amp) 'N engine force'])
for i = 1:fs
   
    disp(['The optimization for the ' num2str(i) 'th frequency (' num2str(f(i)) ' Hz) is started'])
    % The cost function changes as the frequency changes
    Cost_free=@(X) NumericalPower2Integral(Aq(X,w(i)),Xmesh,Ymesh,Zmesh,CavityDim.X,CavityDim.Y,CavityDim.Z,cavity. ModeIndex,dv);
    %Cost=@(X) Kuri_Murales_Cost_Two(Cost_free,X,CavityDim,0.05);
tic
    % The PSO optimization 
    [BestIntPr(i),Qbest(i,:)]=Best_PSO_COMPLETED(Cost_free,opt);
toc    
    % cheking the violation
    violation_speaker1=CONS(Qbest(i,1),Qbest(i,2),Qbest(i,3),CavityDim);
    violation_speaker2=CONS(Qbest(i,5),Qbest(i,6),Qbest(i,7),CavityDim);
    violation_opt(i,:)=[violation_speaker1, violation_speaker2];
    
    
    disp(['The 1st optimal speaker position for this frequency is: ' num2str(Qbest(i,1:3))])
    disp(['The 2nd optimal speaker position for this frequency is: ' num2str(Qbest(i,5:7))])

    disp(['violation of the ' num2str(i) 'th frequency optimization is ' num2str(violation_opt(i,:))])
    Cost_no(i)= Cost_free([0,0,0,0,0,0,0,0]);
end

QbestPositions=Qbest(:,1:3);        % Optimum Position of the secondary sound source
QbestVol=Qbest(:,4);                % Optimum Volume velocity of the secondary sound source
save(['TwoSpeaker_output_with_Force ' num2str(Force.Amp) ' ' ])




clearvars
clc
% close all
Force.Amp=2000
% Data file renamed from the original 'WeightedSensorWithForce L2000 ' (trailing
% space) to 'WeightedSensorWithForce_L2000.mat'. Point this at ../data/weighted_sensor.
load(fullfile('..','data','weighted_sensor', ...
    ['WeightedSensorWithForce_L' num2str(Force.Amp) '.mat']))

ax=gca;
plot(f,20*log(EstimatedPres),'r','LineWidth',2)
hold on
plot(f,20*log(ActualPres),'LineWidth',2)
xlabel('Frequency (Hz)')
ylabel('Pressure (dB)')
ax.XAxis.FontSize = 12;
ax.YAxis.FontSize = 12;
ax.FontWeight = 'bold';

legend('Estimated Pressure','Actual Pressure')
set(gca,'LineWidth',2)

rmsw=zeros(size(Wbest,2),1);
for i=1:size(Wbest,2)
   rmsw(i)=rms(Wbest(:,i));
    
    
    
end
figure
bar(rmsw)
set(gca,'LineWidth',2)
ylabel('Root Mean Square of Weights')
xlabel('number of the sensors')
%  for i=1:size(Wbest,2)
%      figure
%      plot(f,Wbest(:,i))
%      xlabel('Frequency (Hz)')
%      ylabel('Weight Value')
%      ax=gca;
%      ax.XAxis.FontSize = 12;
%      ax.YAxis.FontSize = 12;
%      ax.FontWeight = 'bold';
%      
%  end
figure
plot(f,Wbest(:,1),'LineWidth',2)
hold on
plot(f,Wbest(:,2),'r','LineWidth',2)
hold on
plot(f,Wbest(:,8),'g','LineWidth',2)
datadir = fullfile('..','data','optimization_comparison');
ba=xlsread(fullfile(datadir,'Data_BA.xlsx'));
ga=xlsread(fullfile(datadir,'Data_GA.xlsx'));
gwo=xlsread(fullfile(datadir,'Data_GWO.xlsx'));
pso=xlsread(fullfile(datadir,'Data_PSO.xlsx'));
figure
ax = gca;

plot(log(ba(:,1)),pso(:,2),'b','LineWidth', 2)
hold on
plot(log(ba(:,1)),ga(:,2),'g','LineWidth', 2)
hold on
plot(log(ba(:,1)),ba(:,2),'r','LineWidth', 2)
hold on
plot(log(ba(:,1)),gwo(:,2),'LineWidth', 2)


xlabel('Logarithmic iteration')
ylabel('Best value')
legend('PSO','GA','BA','GWO')
ax.XAxis.FontSize = 12;
ax.YAxis.FontSize = 12;
ax.FontWeight = 'bold';
set(gca,'LineWidth',2)
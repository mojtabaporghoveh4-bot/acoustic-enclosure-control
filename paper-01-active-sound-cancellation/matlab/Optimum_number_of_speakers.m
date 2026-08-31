y=[98 85 70 42 26 17 15.3 15.24 15.2 15.2];
x=[1   2  3  4   5  6  8     9     11   12];

% Error Plot
figure
ax=gca;
plot(x,y,'b','LineWidth',2)

xlabel('Number of Speakers','FontSize',14)
ylabel('Estimation Cumulative Error (dB)','FontSize',14)
ax.XAxis.FontSize = 12;
ax.YAxis.FontSize = 12;
ax.FontWeight = 'bold';
set(gca,'LineWidth',2)
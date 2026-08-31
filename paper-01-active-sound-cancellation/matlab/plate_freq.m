function [radialfreq,index]=plate_freq(plate)
% this function obtains the natural frequencies of the plate with specified
% mode numbers, it also obtains te mode indexes

m=1:plate.mode;

% All the possible mode indexes

[m1,m2]=meshgrid(m,m);sizpl=size(m1);   

% Plate natural frequencies

w_p=sqrt(plate.bending/(plate.thickness*plate.density)) * ( (m1.*pi/plate.dim.x).^2 + (m2*pi/plate.dim.y).^2  );

% sorting natural frequencies 

radialfreq=sort(w_p(:));

% selecting the first plate.modes of the natural frequencies

radialfreq=radialfreq(1:plate.mode);

% preallocating the indexes

M1=zeros(plate.mode,1);M2=M1;index=zeros(plate.mode,2);

% finding the indexes

for i=1:plate.mode
    
b=find(w_p==radialfreq(i)); % b is corresponded to the i'th natural frequency
    if numel(b)>1
         b=min(b);
    end
[M1(i,:),M2(i,:)]=ind2sub(sizpl,b); % returns the values corresponding to the i'th natural frequency
index(i,:)=[m1( M1(i,:) , M2(i,:) ), m2( M1(i,:) , M2(i,:) )];

end


end
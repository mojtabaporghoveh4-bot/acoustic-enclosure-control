function [radialfreq,index]=cavity_freq(cavity)
% This function calculates the natural frequency of the cavity as well as
% the modal indices of the cavity. The inputs of the function are: Cavity 
% Mode Number and size of the cavity 
n=0:cavity.mode;
[n1,n2,n3]=meshgrid(n,n,n);sizac=size(n1);
N1=zeros(cavity.mode,1);N2=N1;N3=N1;
index=zeros(cavity.mode,3);
w_c=pi*cavity.sndspeed*sqrt (  (n1/cavity.dim.x).^2 + (n2/cavity.dim.y).^2 + (n3/cavity.dim.z).^2 );
radialfreq=sort(w_c(:));
radialfreq=unique(radialfreq);
radialfreq=radialfreq(1:cavity.mode);
% Modal Indexes

    for i=1:cavity.mode
        b=find(w_c==radialfreq(i));
            if numel(b)>1
                 b=min(b);
            end
    [N1(i,:),N2(i,:),N3(i,:)]=ind2sub(sizac,b);
    index(i,:)=[n1(N1(i,:),N2(i,:),N3(i,:)),n2(N1(i,:),N2(i,:),N3(i,:)),n3(N1(i,:),N2(i,:),N3(i,:))];
    
    end


end
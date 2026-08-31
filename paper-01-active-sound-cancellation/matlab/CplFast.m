function y=CplFast(plate,cavity,j,i) % Coupling Matrix

v=size( find ( cavity.ModeIndex(j,:) ),2 ); % v is the number of nonzero parameters of the modal indices
er=sqrt(2).^v;
n=cavity.ModeIndex(j,:);
m=plate.ModeIndex(i,:);
s=2*plate.area*er*(-1)^n(3);    m1=m(1);m2=m(2);n1=n(1);n2=n(2);
    if n1~=m1 && n2~=m2
         y= s* ( m1*m2*   ((-1)^(n1+m1)-1)* ((-1)^(n2+m2)-1) )/( (pi^2)*(n1^2-m1^2)*(n2^2-m2^2) );

    else
        y=0;
    end

end
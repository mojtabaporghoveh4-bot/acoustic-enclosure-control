function y=Kuri_Murales_Cost_PSO(fun,X,CavityDim,epsilon)

    if abs(CONS(X(1),X(2),X(3),CavityDim))<epsilon
    
        y=fun(X);
    
    else
       
        y=10^(9)*ones(size(X,1),1);
        
    end



end
function y=VNonZeros(matrix)
% this function calculates the number of nonzero arrays of each rows of
% the matrix

n=size(matrix,1);   % Number of rows
y=zeros(n,1);

    for i=1:n
        y(i)=nnz(matrix(i,:));
    end






end
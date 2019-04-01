function T_inv = inverse_trans_matrix(T)
Rot = T(1:3,1:3);
O = T(1:3,4);
T_inv = zeros(4,4);
T_inv(1:3,1:3) = Rot';
T_inv(1:3,4) = -Rot'*O;
T_inv(4,4) = 1;
end
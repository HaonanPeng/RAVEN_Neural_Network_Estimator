close all, clear all, clc


ball_centers = [1,0,0;
               0 1 0;
               0 0 1];
           
p1 = ball_centers(1,:);
p2 = ball_centers(2,:);
p3 = ball_centers(3,:);

x = ( (p2(2)-p1(2))*(p3(3)-p1(3))-(p2(3)-p1(3))*(p3(2)-p1(2)) );
y = ( (p2(3)-p1(3))*(p3(1)-p1(1))-(p2(1)-p1(1))*(p3(3)-p1(3)) );
z = ( (p2(1)-p1(1))*(p3(2)-p1(2))-(p2(2)-p1(2))*(p3(1)-p1(1)) );

norm = [x,y,z]/sqrt(x^2+y^2+z^2)

syms cx cy cz d1x d1y d1_z d2_x d2_y d2_z 

eqn_1 = 

function eqn = end_effector_PR(x) 
    T=ravenFK(x(1),x(2),x(3),x(4),x(5),x(6));
    T_takeout = T(1:3,:);
    
    eqn = [];
    for iter = 1:12
        eqn = [eqn;T_takeout(iter)-T_fact_takeout(iter)];
    end
end

options = optimoptions('fsolve','FunctionTolerance',1e-100,'StepTolerance',1e-100,'MaxIter',10000,'Display','off');
input = fsolve(@IK,initial_guess,options);

        





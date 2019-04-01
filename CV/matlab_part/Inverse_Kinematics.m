close all, clear all, clc

input = inverse_kinematics()

function input = inverse_kinematics()
% syms th1 th2 d3 th4 th5 th6

% th1_ref = 0;
% th2_ref = 0;
% d3_ref = 0;
% th4_ref = 0;
% th5_ref = 0;
% th6_ref = 0;

th1_ref = rand(1);
th2_ref = rand(1);
d3_ref = rand(1);
th4_ref = rand(1);
th5_ref = rand(1);
th6_ref = rand(1);

th1_fact = th1_ref+rand(1)*0.01;
th2_fact = th2_ref+rand(1)*0.02;
d3_fact = d3_ref+rand(1)*0.03;
th4_fact = th4_ref+rand(1)*0.04;
th5_fact = th5_ref+rand(1)*0.05;
th6_fact = th6_ref+rand(1)*0.06;

T_fact = ravenFK(th1_fact,th2_fact,d3_fact,th4_fact,th5_fact,th6_fact);
T_fact_takeout = T_fact(1:3,:);

fprintf('initial guess:')
initial_guess = [th1_ref,th2_ref,d3_ref,th4_ref,th5_ref,th6_ref]

fprintf('fact value:')
fact_value = [th1_fact,th2_fact,d3_fact,th4_fact,th5_fact,th6_fact]

function eqn = IK(x) 
    T=ravenFK(x(1),x(2),x(3),x(4),x(5),x(6));
    T_takeout = T(1:3,:);
    
    eqn = [];
    for iter = 1:12
        eqn = [eqn;T_takeout(iter)-T_fact_takeout(iter)];
    end
end

options = optimoptions('fsolve','FunctionTolerance',1e-100,'StepTolerance',1e-100,'MaxIter',10000,'Display','off');
input = fsolve(@IK,initial_guess,options);
end

close all, clear all, clc

% T_fact: T matrix of end effector 
% initial_guess: joint angle from RAVEN_state,[theta1 2 3 4 5 6]
input = inverse_kinematics(T_fact,initial_guess)

function input = inverse_kinematics(T_fact,initial_guess)
T_fact_takeout = T_fact(1:3,:);

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

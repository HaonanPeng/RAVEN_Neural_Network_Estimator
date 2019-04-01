close all, clear all, clc
syms t

%time samples from (1:10000)s
sample_time = 10000;

data = zeros(6,sample_time);
% theta_1,2,3,4,5,6_encoder_value -- (6)

samples = zeros(3+3+9,sample_time); 
% detected_endeffector_x,y,z -- (3)
% detected_endeffector_roll,pitch,yaw(rads) --(3)
% detected_endeffector_rotationMatrix(:,1),(:,2),(:,3) --(9)

%% encoder operates in linear and error in linear
t = 1:sample_time;

t_encoder_1 = t*0.00016;
t_encoder_1_fact = t_encoder_1*1.06;

t_encoder_2 = t*0.00015;
t_encoder_2_fact = t_encoder_2*1.05;

d_encoder_3 = t*0.000014;
d_encoder_3_fact = d_encoder_3*1.04;

t_encoder_4 = t*0.00013;
t_encoder_4_fact = t_encoder_4*1.03;

t_encoder_5 = t*0.00012;
t_encoder_5_fact = t_encoder_5*1.02;

t_encoder_6 = t*0.00011;
t_encoder_6_fact = t_encoder_6*1.01;

%% create sample data

data(1:6,:) = [t_encoder_1;t_encoder_2;d_encoder_3;t_encoder_4;t_encoder_5;t_encoder_6];
t_sample = [t_encoder_1_fact;t_encoder_2_fact;d_encoder_3_fact;t_encoder_4_fact;t_encoder_5_fact;t_encoder_6_fact];                       

for time = 1:sample_time
    T=double(ravenFK(t_sample(1,time),t_sample(2,time),t_sample(3,time),t_sample(4,time),t_sample(5,time),t_sample(6,time)));
    samples(1:3,time) = T(1:3,4);
    samples(4:6,time) = rotm2eul(T(1:3,1:3));
    samples(7:9,time) = T(1:3,1);
    samples(10:12,time) = T(1:3,2);
    samples(13:15,time) = T(1:3,3);
end

%% save
save('data.txt', 'data', '-ascii', '-single', '-tabs')
save('samples.txt', 'samples', '-ascii', '-single', '-tabs')



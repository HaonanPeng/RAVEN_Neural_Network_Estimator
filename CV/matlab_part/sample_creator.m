close all, clear all, clc
syms t


%time samples from (1:10000)s
sample_time = 10000;

data_RPY = zeros(6+3+3,sample_time);
% theta_1,2,3,4,5,6_encoder_value -- (6)
% detected_endeffector_x,y,z -- (3)
% detected_endeffector_roll,pitch,yaw(rads) --(3)

data_RotationMatrix = zeros(6+3+9,sample_time);
% theta_1,2,3,4,5,6_encoder_value -- (6)
% detected_endeffector_x,y,z -- (3)
% detected_endeffector_rotationMatrix(:,1),(:,2),(:,3) --(9)



samples_RPY = zeros(3+3,sample_time); 
% detected_endeffector_x,y,z -- (3)
% detected_endeffector_roll,pitch,yaw(rads) --(3)

samples_RotationMatrix = zeros(3+9,sample_time); 
% detected_endeffector_x,y,z -- (3)
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
t_data = zeros(6,sample_time);
t_data(1:6,:) = [t_encoder_1;t_encoder_2;d_encoder_3;t_encoder_4;t_encoder_5;t_encoder_6];
t_sample = [t_encoder_1_fact;t_encoder_2_fact;d_encoder_3_fact;t_encoder_4_fact;t_encoder_5_fact;t_encoder_6_fact];      

data_RPY(1:6,:) = t_data;
data_RotationMatrix(1:6,:) = t_data;


for time = 1:sample_time
    T_data = double(ravenFK(t_data(1,time),t_data(2,time),t_data(3,time),t_data(4,time),t_data(5,time),t_data(6,time)));
    T_sample = double(ravenFK(t_sample(1,time),t_sample(2,time),t_sample(3,time),t_sample(4,time),t_sample(5,time),t_sample(6,time)));
    
    data_RPY(7:9,time) = T_data(1:3,4);
    data_RPY(10:12,time) = rotm2eul(T_data(1:3,1:3));
    
    data_RotationMatrix(7:9,time) = T_data(1:3,4);
    data_RotationMatrix(10:12,time) = T_data(1:3,1);
    data_RotationMatrix(13:15,time) = T_data(1:3,2);
    data_RotationMatrix(16:18,time) = T_data(1:3,3);
    
    samples_RPY(1:3,time) = T_sample(1:3,4);
    samples_RPY(4:6,time) = rotm2eul(T_sample(1:3,1:3));
    
    samples_RotationMatrix(1:3,time) = T_sample(1:3,4);
    samples_RotationMatrix(4:6,time) = T_sample(1:3,1);
    samples_RotationMatrix(7:9,time) = T_sample(1:3,2);
    samples_RotationMatrix(10:12,time) = T_sample(1:3,3);
end

save('data_RPY.txt', 'data_RPY', '-ascii', '-single', '-tabs')
save('data_RotationMatrix.txt', 'data_RotationMatrix', '-ascii', '-single', '-tabs')
save('samples_RPY.txt', 'samples_RPY', '-ascii', '-single', '-tabs')
save('samples_RotationMatrix.txt', 'samples_RotationMatrix', '-ascii', '-single', '-tabs')



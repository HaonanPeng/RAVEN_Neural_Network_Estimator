close all, clear all, clc

raven_state = importdata('data_files/raven_state_traj13.txt');
result_file_name = 'data_files/raven_state_traj13_toggled.txt';

size_ravenstate = size(raven_state);
toggle_rate = 10;

% filter data
for col_index = 2:size_ravenstate(2)
raven_state(: , col_index) = filter_exp_decay(raven_state(: , col_index) , 0.95);
end

% toggle data
line_idx = 1;
for tog_index = 1: toggle_rate : size_ravenstate(1)
    raven_state_toggled(line_idx, :) =  raven_state(tog_index,:);
    line_idx = line_idx +1;
end

dlmwrite(result_file_name,raven_state_toggled,'precision',16,'delimiter',' ')
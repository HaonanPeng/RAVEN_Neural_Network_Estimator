close all, clear all, clc

raven_state = importdata('data_files/raven_state_traj11.txt');

size_ravenstate = size(raven_state);

% filter data
for col_index = 2:size_ravenstate(2)
raven_state(: , col_index) = filter_exp_decay(raven_state(: , col_index) , 0.95);
end

% toggle data
line_idx = 1;
for tog_index = 1: 10 : size_ravenstate(1)
    raven_state_toggled(line_idx, :) =  raven_state(tog_index,:);
    line_idx = line_idx +1;
end

dlmwrite('data_files/raven_state_traj11_toggled.txt',raven_state_toggled,'precision',16,'delimiter',' ')
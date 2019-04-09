function filtered_array = moving_average_filter(array , windowSize)

filter_b = (1/windowSize)*ones(1,windowSize);
filter_a = 1;

filtered_array_raw = filter(filter_b,filter_a, array );
filtered_array = filtered_array_raw(:,1:end);

end
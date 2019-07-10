function filtered_array = filter_exp_decay(input_array , beta)

size_array = size(input_array);

filtered_array = input_array;


for idx = 2:size_array
    filtered_array(idx) = (beta*filtered_array(idx-1)+(1-beta)*input_array(idx));
end


end
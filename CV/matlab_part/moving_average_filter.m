function filtered_array = moving_average_filter(array , windowSize)

%[IMPT] window size must be odd
filtered_array = zeros(size(array));

m = (windowSize - 1) / 2;

first_terms = array(1:m);
last_terms = array(end-m+1:end);

extended_array = [first_terms ; array ; last_terms];


for idx = 1 : length(array)
    filtered_array(idx) = sum(extended_array(idx:(idx+windowSize-1)))/windowSize;
end

end
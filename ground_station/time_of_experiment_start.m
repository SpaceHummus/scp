function t0 = time_of_experiment_start(image_directory)
% This function returns hard coded time of the start of the experiment (t0)

if contains(image_directory,'ISS')
    t0 = datenum(2022,02,22,12,30,0);
elseif contains(image_directory,'Earth')
    t0 = datenum(2022,02,16,20,52,0);
else
    error('Unknown experiment in %s',image_directory);
end
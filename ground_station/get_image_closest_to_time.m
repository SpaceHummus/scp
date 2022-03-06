function [img_path,t_hours_out] = get_image_closest_to_time(image_directory,t_hours,camera_filter)
% image_directory - directory that contains all images to select from
% t_hours - number of hours from experiment start to get the image
% camera_filter - which camera to use (CA,CB,CC,CD,C0,C1) and focus.
%   for example CA_F0310

%% Input checks
if ~exist('image_directory','var') || isempty(image_directory)
    image_directory = 'C:\_AvivLabs\ISSModule\03 Raw Images';
end

if ~exist('camera_filter','var') || isempty(camera_filter)
    camera_filter = 'CA_F0310';
end

%% Figure out what is time zero
t0 = time_of_experiment_start(image_directory);

%% Load all images and find closest
ds = fileDatastore([image_directory '\*' camera_filter '.jpg'],'ReadFcn',@imread);
times = cellfun(@time_picture_was_taken,ds.Files);
times_hr = (times-t0)*24;

%% Find the closest image
[~,i] = min(abs(times_hr-t_hours));
img_path = ds.Files{i};
t_hours_out = times_hr(i);

if abs(t_hours_out-t_hours) > 1
    % We couldn't find an image that is less than one hour away
    img_path = '';
end
% This script generates a comparison between ISS and Earth

%% Get Inputs
base_earth_input_folder = ['..\..\EarthControl\images\'];
base_iss_input_folder = ['..\..\ISSModule\03 Raw Images\'];

% What times to include in the picture
t_hr = 1:1:(11*24);

if false
    % Output file path
    video_file_name = '..\..\SpaceVsEarth_ControlChamber.mp4';

    % Camera filters
    camera_filter_iss = 'CA_F0310';
    camera_filter_earth = 'CA_F0080';
    
    % Keep empty if no image crop is needed
    focus_area_x_earth = 900:3300;
    focus_area_y_earth = 800:2000;
    focus_area_x_iss = 900:3300;
    focus_area_y_iss = 1050:2250;
    
else
    % Output file path
    video_file_name = '..\..\SpaceVsEarth_FarRedChamber.mp4';

    % Camera filters
    camera_filter_iss = 'CD_F0270';
    camera_filter_earth = 'CD_F0100';
    
    % Keep empty if no image crop is needed
    focus_area_x_earth = 900:3300;
    focus_area_y_earth = 950:2150;
    focus_area_x_iss = 900:3300;
    focus_area_y_iss = 900:2100;
end


%% Prep

% Delete file if already exist
if exist(video_file_name,'file')
    delete(video_file_name);
end

% texts
earth_name_im = text2img('Earth',20);
iss_name_im = text2img('Space',20);

% Open video
v = VideoWriter(video_file_name,'MPEG-4');
v.FrameRate = 15;
open(v);

%% Main loop
im_black = zeros(3040,4056,3,'uint8');
for i=1:length(t_hr)
    t = t_hr(i);
    
    % Generate t in text
    t_im = text2img(sprintf('%.0f days %.0f hours',floor(t/24),t-floor(t/24)*24));
    
    %% Load images
    im_e_path = get_image_closest_to_time(base_earth_input_folder,t,camera_filter_earth);
    if ~isempty(im_e_path)
        try
            im_e = imread(im_e_path);
        catch
            im_e = im_black;
        end
    else
        im_e = im_black;
    end
    
    im_iss_path = get_image_closest_to_time(base_iss_input_folder,t,camera_filter_iss);
    if ~isempty(im_iss_path)
        try
            im_iss = imread(im_iss_path);
        catch
            im_iss = im_black;
        end
    else
        im_iss = im_black;
    end
   
    %% Concatinate and draw
    % Trim focus area
    if ~isempty(focus_area_x_earth)
        im_e = im_e(focus_area_y_earth,focus_area_x_earth,:);
        im_iss = im_iss(focus_area_y_iss,focus_area_x_iss,:);
    end
    
    % Add text
    im_e = add_title(im_e,earth_name_im);
    im_e = add_title(im_e,t_im,'bottomleft');
    im_iss = add_title(im_iss,iss_name_im);
    
    im = [im_iss;(im_iss(1:3,:,:)*0);im_e];
    writeVideo(v,im);
    imshow(im);
    pause(0.1);
end
close(v);

function im = add_title(im,imt,place)

if ~exist('place','var')
    place = 'topcenter';
end

sz_i = size(im);
sz_t = size(imt);

switch(lower(place))
    case 'topcenter'
        im((1:sz_t(1)), ...
            round(sz_i(2)/2)+(1:sz_t(2))-round(sz_t(2)/2),:) = imt;
    case 'bottomleft'
        im(sort(sz_i(1)-(1:sz_t(1))+1), ...
           (1:sz_t(2)),:) = imt;
end
end
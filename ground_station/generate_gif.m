%% Inputs
base_folder = '..\..\EarthControl\';
base_input_folder = [base_folder 'images\'];

base_folder = '..\..\ISSModule\';
base_input_folder = [base_folder '03 Raw Images\'];

switch('med')
    case 'AC'
        output_file_name = [base_folder 'AC Animated.gif'];
        ds1 = fileDatastore([base_input_folder '\*CC_F0080.jpg'],'ReadFcn',@imread);
        ds2 = fileDatastore([base_input_folder '\*CA_F0080.jpg'],'ReadFcn',@imread);
    case 'BD'
        output_file_name = [base_folder 'BD Animated.gif'];
        ds1 = fileDatastore([base_input_folder '\*CB_F0060.jpg'],'ReadFcn',@imread);
        ds2 = fileDatastore([base_input_folder '\*CD_F0100.jpg'],'ReadFcn',@imread);
    case 'AD'
        output_file_name = [base_folder 'Ctrl_FR Animated.gif'];
        ds1 = fileDatastore([base_input_folder '\*CA_F0080.jpg'],'ReadFcn',@imread);
        ds2 = fileDatastore([base_input_folder '\*CD_F0100.jpg'],'ReadFcn',@imread);
    case 'med'
        output_file_name = [base_folder 'med.gif'];
        ds1 = fileDatastore([base_input_folder '\*C0.jpg'],'ReadFcn',@imread);
        ds2 = fileDatastore([base_input_folder '\*C1.jpg'],'ReadFcn',@imread);
end

frame_freq_hr = 2; 0.5; % Pick one frame every x hours

% Set start and end times for the video
t_start_hr = 0;

%% Set figure
h = figure(1);
set(h,'units','normalized','outerposition',[0 0 1 1])
axis tight manual % this ensures that getframe() returns a consistent size

video_file_name = strrep(output_file_name,'.gif','.mp4');

if exist(output_file_name,'file')
    delete(output_file_name);
end
if exist(video_file_name,'file')
    delete(video_file_name);
end

v = VideoWriter(video_file_name,'MPEG-4');
v.FrameRate = 15;
open(v);
%% Figure out time
t_0 = time_of_experiment_start(base_input_folder);
t_end = time_picture_was_taken(ds1.Files{end});

%% 
firstNightImage = true;
clear isEnvelop
t_image = t_0-1;
never_wrote = true;
for n = 1:length(ds1.Files)
    try
    t = time_picture_was_taken(ds1.Files{n});
    
    if (t-t_0)*24 < t_start_hr
        continue;
    end
    
    if ((t-t_image)*24 < frame_freq_hr)
        continue;
    elseif (t-t_image)*24 > frame_freq_hr*2
        t_image = t;
    else
        t_image = t_image+frame_freq_hr/24;
    end
    
    imA = imread(ds1.Files{n});
    imB = imread(ds2.Files{n});

    if mean(double(imA(:))) < 10
        if ~firstNightImage
            continue;
        else
            firstNightImage = false;
        end
    else
        firstNight = true;
    end
    
    % Calculate time from experiment start and put in the right format
    dt_hours = (t-t_0)*24;
    dt_days = floor(dt_hours/24);
    dt_hours_part = dt_hours - dt_days*24;
    ttl = sprintf('%.0f Days %02.1f Hours From Experiment Start',...
        dt_days,dt_hours_part);
   
    subplot(1,6,1:3);
    imshow(imA);
    title(ttl);
    subplot(1,6,4:6);
    imshow(imB);

    drawnow 
    % Capture the plot as an image 
    frame = getframe(h); 
    im = frame2im(frame); 

    if ~exist('isEnvelop','var')
        isEnvelop = im(:,:,1) == 240 & im(:,:,2) == 240 & im(:,:,3) == 240;
    end
    
    isAllEnvelop1 = all(isEnvelop,2);
    isAllEnvelop2 = all(isEnvelop,1);
    im(isAllEnvelop1,:,:) = [];
    im(:,isAllEnvelop2,:) = [];

    [imind,cm] = rgb2ind(im,256); 
    % Write to the GIF File 
    if never_wrote
      never_wrote=false;
      imwrite(imind,cm,output_file_name,'gif', 'Loopcount',inf); 
    else
      imwrite(imind,cm,output_file_name,'gif','WriteMode','append'); 
    end 
    
    % Write to video
    writeVideo(v,im);
    catch e
    end
end
  
close(v);
close(h);


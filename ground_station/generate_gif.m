%% Inputs
output_file_name = 'animated.gif';
base_input_folder = '..\images'; % Input images folder (03 Raw Images)

ds1 = fileDatastore([base_input_folder '\*CA_F0130.jpg'],'ReadFcn',@imread);
ds2 = fileDatastore([base_input_folder '\*CC_F0130.jpg'],'ReadFcn',@imread);

frame_freq_hr = 0.5; % Pick one frame every x hours

% Set start and end times for the video
t_start_hr = 0;

%% Set figure
h = figure(1);
set(h,'units','normalized','outerposition',[0 0 1 1])
axis tight manual % this ensures that getframe() returns a consistent size

[~,video_name] = fileparts(output_file_name);
v = VideoWriter(video_name,'MPEG-4');
v.FrameRate = 15;
open(v);
%% Figure out time
t_0 = time_of_first_picture(base_input_folder);
t_end = time_picture_was_taken(ds1.Files{end});


time_format = 'hours';

%% 
firstNightImage = true;
clear isEnvelop
t_image = t_0-1;
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

   
    subplot(1,6,1:3);
    imshow(imA);
    switch(time_format)
        case 'days'
            title(sprintf('%.2f Days From Experiment Start',t-t_0));
        case 'hours'
            title(sprintf('%.1f Hours From Experiment Start',(t-t_0)*24));
    end
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
    if n == 1 
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


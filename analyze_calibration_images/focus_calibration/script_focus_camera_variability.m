% This script computes camera to camera variability of the focus setting

%% Get all camera models
ds = fileDatastore('C*.mat','ReadFcn',@load);

clear data;
camera_names = {};
for i=1:length(ds.Files)
    [~,f] = fileparts(ds.Files{i});
    d = ds.read();
    
    camera_name = f(1:3);
    
    if ~any(strcmp(camera_names,camera_name))
        % New camera add to data
        if ~exist('data','var')
            data = d;
        else
            data(end+1) = d;
        end
        camera_names{end+1} = camera_name;
    end
end

%% Concatinate data
h = data(1).h;
recommendend_focus_setting = [data(:).recommended_focus_setting];

%% Plot data as is
figure(14);
subplot(3,1,[1 2]);
plot(h,recommendend_focus_setting,'-*');
grid on;
%xlabel('Height [mm]');
ylabel('Recommended Focus Setting');
ylim([0 400]);
legend(camera_names)

subplot(3,1,3);
plot(h,recommendend_focus_setting-mean(recommendend_focus_setting,2));
grid on;
xlabel('Height [mm]');
ylabel('Diff from Mean');

%% See if a constant correction makes a significant difference
adjusted_f = recommendend_focus_setting - mean(recommendend_focus_setting);

figure(15);
subplot(3,1,[1 2]);
plot(h,adjusted_f,'-*');
grid on;
%xlabel('Height [mm]');
ylabel('Adjusted Recommended Focus Setting');
legend(camera_names)
title('What Happens When Correcting For Offset');

subplot(3,1,3);
plot(h,adjusted_f-mean(adjusted_f,2),'-*');
grid on;
xlabel('Height [mm]');
ylabel('Diff from Mean');
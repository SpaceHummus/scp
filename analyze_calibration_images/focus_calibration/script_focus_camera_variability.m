% This script computes camera to camera variability of the focus setting


%% Input
camera_name = 'C05';

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

%% Plot

figure(14);
subplot(3,1,[1 2]);
plot(h,recommendend_focus_setting);
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


return;
xlabel('Height [mm]');
ylabel('Measurment/Robot Stability');
title('Recommended Focus Setting');
legend('Robot Reset 1','Robot Reset 2','Robot Reset 3','Robot Reset 4');
grid on;

m = [a.recommended_focus_setting(:) b.recommended_focus_setting(:) c.recommended_focus_setting(:) d.recommended_focus_setting(:)];
m = mean(m,2);

subplot(2,1,2);
plot(...
    a.h,a.recommended_focus_setting-m,'*-',...
    b.h,b.recommended_focus_setting-m,'*-',...
    c.h,c.recommended_focus_setting-m,'*-',...
    d.h,d.recommended_focus_setting-m,'*-'...
    );
title('Deviation from Mean');
xlabel('Height [mm]');
ylabel('Focus Setting Diff');
grid on;




return;

h = data(1).h;
calibration_date = {data(:).calibration_date};
recommendend_focus_setting = [data(:).recommended_focus_setting];
   
figure(13);
subplot(3,1,[1 2]);
plot(h,recommendend_focus_setting)
grid on;
%xlabel('Height [mm]');
ylabel('Recommended Focus Setting');
ylim([0 400]);
if (length(calibration_date) == 2)
    legend([calibration_date{1} 'Before Vibration Testing'],[calibration_date{2} ' After Vibration Testing']);
else
    legend(calibration_date{1},[calibration_date{2} 'Before Vibration Testing'],[calibration_date{3} ' After Vibration Testing']);
end

subplot(3,1,3);
plot(h,recommendend_focus_setting-mean(recommendend_focus_setting,2));
grid on;
xlabel('Height [mm]');
ylabel('Diff from Mean');




clear;

%% Single Camera After Shakes
a = load('C02_focus_setting_21-12-19-2.mat');
b = load('C02_focus_setting_21-12-19-3.mat');

figure(13);
subplot(2,1,1);
plot(a.h,a.recommended_focus_setting,'*-',b.h,b.recommended_focus_setting,'*-');
xlabel('Height [mm]');
ylabel('Impact of Shaking Camrea');
legend('Before Shake','After Shake');
grid on;
title('Recommended Focus Setting');

subplot(2,1,2);
plot(a.h,a.recommended_focus_setting-b.recommended_focus_setting,'*-');
title('Before - After Shake');
xlabel('Height [mm]');
ylabel('Focus Setting Diff');
grid on;


%% Robot Stability

% Load images after robot reset
a = load('C02_focus_setting_21-12-19-1.mat');
b = load('C02_focus_setting_21-12-19-2.mat');
c = load('C02_focus_setting_21-12-19-3.mat');
d = load('C02_focus_setting_2021-12-20.mat');

figure(14);
subplot(2,1,1);
plot(...
    a.h,a.recommended_focus_setting,'*-',...
    b.h,b.recommended_focus_setting,'*-',...
    c.h,c.recommended_focus_setting,'*-',...
    d.h,d.recommended_focus_setting,'*-');
xlabel('Height [mm]');
ylabel('Measurment/Robot Stability');
title('Recommended Focus Setting');
legend('Robot Reset 1','Robot Reset 2','Robot Reset 3','Robot Reset 4');
grid on;

m = [a.recommended_focus_setting(:) b.recommended_focus_setting(:) c.recommended_focus_setting(:) d.recommended_focus_setting(:)];
m = mean(m,2);

subplot(2,1,2);
plot(...
    a.h,a.recommended_focus_setting-m,'*-',...
    b.h,b.recommended_focus_setting-m,'*-',...
    c.h,c.recommended_focus_setting-m,'*-',...
    d.h,d.recommended_focus_setting-m,'*-'...
    );
title('Deviation from Mean');
xlabel('Height [mm]');
ylabel('Focus Setting Diff');
grid on;

%% Camera Variation

% Load images after robot reset
a = load('C02_focus_setting_2021-12-20.mat');
b = load('C03_focus_setting_2021-12-20.mat');
c = load('C04_focus_setting_2021-12-21.mat');
d = load('C05_focus_setting_2021-12-21.mat');

figure(15);
subplot(2,1,1);
plot(...
    a.h,a.recommended_focus_setting,'*-',...
    b.h,b.recommended_focus_setting,'*-',...
    c.h,c.recommended_focus_setting,'*-',...
    d.h,d.recommended_focus_setting,'*-'...
    )
xlabel('Height [mm]');
ylabel('Recommended Focus Setting');
title('Camera Differences');
legend('C02','C03','C04','C05');
grid on;

m = [a.recommended_focus_setting(:) b.recommended_focus_setting(:) ...
    c.recommended_focus_setting(:) d.recommended_focus_setting(:)];
m = mean(m,2);

subplot(2,1,2);
plot(...
    a.h,a.recommended_focus_setting-m,'*-',...
    b.h,b.recommended_focus_setting-m,'*-',...
    c.h,c.recommended_focus_setting-m,'*-',...
    d.h,d.recommended_focus_setting-m,'*-'...
    );
title('Deviation from Mean');
xlabel('Height [mm]');
ylabel('Focus Setting Diff');
grid on;

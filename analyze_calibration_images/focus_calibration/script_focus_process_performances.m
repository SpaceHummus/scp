% This script uses demo focus settings to estimate performances

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

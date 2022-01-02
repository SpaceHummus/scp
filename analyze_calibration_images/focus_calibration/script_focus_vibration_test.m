% This script tacks focus performances after vibration tests

%% Input
camera_name = 'C05';

%% Compute vibration impact
ds = fileDatastore([camera_name '*.mat'],'ReadFcn',@load);

clear data
for i=1:length(ds.Files)
    data(i) = ds.read();
end

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
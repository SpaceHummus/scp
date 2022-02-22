% This script generates overview of the telemetry file

telemetry_csv_path = '../Earth Backup/telematry.csv';

%% Read data
fid = fopen(telemetry_csv_path);
c = textscan(fid,'%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s','Delimiter',',');
fclose(fid);

%% Pars
titles = cell(length(c),1);
for i=1:length(titles)
    titles{i} = c{i}{1};
end

date_time = cellfun(@getdatetime,c{1}(2:end));
days_from_exp_start = date_time-date_time(1);

SW_LED_on = cellfun(@isswon,c{2}(2:end));
SW_air_sensir_on = cellfun(@isswon,c{2}(3:end));
SW_air_medetronic_on = cellfun(@isswon,c{3}(3:end));
BME680_Temperature_C = cellfun(@getscalarparameter,c{6}(2:end));
BME680_Gas_Ohm = cellfun(@getscalarparameter,c{7}(2:end));
BME680_Humidity_Percent = cellfun(@getscalarparameter,c{8}(2:end)); 
BME680_Pressure_hPa = cellfun(@getscalarparameter,c{9}(2:end)); 
VEML7700_1_Lux = cellfun(@getscalarparameter,c{11}(2:end));
VEML7700_2_Lux = cellfun(@getscalarparameter,c{13}(2:end));
INA260_Current_A = cellfun(@getscalarparameter,c{14}(2:end))/1e3;
INA260_Power_W = cellfun(@getscalarparameter,c{16}(2:end))/1e3;
RPI_CPU_Temperature_C = cellfun(@getscalarparameter,c{21}(2:end));
RPI_Used_Space_Percent = cellfun(@getscalarparameter,c{23}(2:end));

states = c{2}(2:end);
mods = {'Booting_0','Booting_1','Booting_2',...
    'Off->day_shade_TransitionStep0','Off->day_shade_TransitionStep3','Off->day_shade_TransitionStep4','Off->day_shade_TransitionStep5',...
    'day_shade','day_shade->Off_TransitionStep0','day_shade->Off_TransitionStep1','day_shade->Off_TransitionStep2',...
    };

states_num = zeros(size(VEML7700_2_Lux));
for imods = 1:length(mods)
    i = when_is_state(states,mods{imods});

    states_num(i) = imods;
end

%% Overview graph
figure(1);
clear ax;

subplot(2,2,1);
plot(days_from_exp_start,BME680_Temperature_C,'o',days_from_exp_start,RPI_CPU_Temperature_C,'o');
title('Temperatures');
xlabel('Days from Experiment Start');
ylabel('Temperature [C]');
ylim([0 60]);
legend('BME','CPU');
grid on;
ax(1) = gca;

subplot(2,2,2);
%i = when_is_state(states,'day_shade');
i = 1:length(days_from_exp_start);
plot(days_from_exp_start(i),VEML7700_1_Lux(i),'o', ...
     days_from_exp_start(i),VEML7700_2_Lux(i),'o');
title('Lux (Day Shade Mode)');
xlabel('Days from Experiment Start');
ylabel('Lumination [Lux]');
legend('VEML7700-1 [Exp]','VEML7700-2 [Ctrl]');
grid on;
ax(2) = gca;

subplot(2,2,3);
plot(days_from_exp_start,INA260_Current_A,'o' ...
     );
title('INA Current [A]');
xlabel('Days from Experiment Start');
ylabel('Current [A]');
legend('INA');
grid on;
ax(3) = gca;

subplot(2,2,4);
plot(days_from_exp_start,states_num,'-*')
title('States');
yticks(1:length(mods))
yticklabels(cellfun(@(x)(strrep(x,'_','-')),mods,'UniformOutput',false))
xlabel('Days from Experiment Start');
grid on;
ax(4) = gca;

linkaxes(ax,'x');

%% Plot per logic state stats
figure(2);

vals = zeros(length(mods),3);
for imods = 1:length(mods)
    i = when_is_state(states,mods{imods});

    vals(imods,1) = nanmean(VEML7700_1_Lux(i));
    vals(imods,2) = nanmean(VEML7700_2_Lux(i));
    vals(imods,3) = nanmean(INA260_Power_W(i));
end
     
subplot(1,2,1);
bar(1:length(mods),vals(:,1:2));
title('Lux Per Mode');
xticks(1:length(mods))
xticklabels(cellfun(@(x)(strrep(x,'_','-')),mods,'UniformOutput',false))
ylabel('Lumination [Lux]');
legend('VEML7700-1 [Exp]','VEML7700-2 [Ctrl]');
xtickangle(45)

subplot(1,2,2);
bar(1:length(mods),vals(:,3));
title('Power Consumtion Per Mode');
xticks(1:length(mods))
xticklabels(cellfun(@(x)(strrep(x,'_','-')),mods,'UniformOutput',false))
ylabel('Power Consumtion[W]');
legend('INA Power[W]');
xtickangle(45)

%%

% Grid of one hour
%Estimate for each hour using the transitions in this hour
t_grid = min(days_from_exp_start):(2/24):max(days_from_exp_start);
led_sw_current_A = NaN*t_grid; 
fr_current_A = NaN*t_grid; 
neopixel_current_A = NaN*t_grid;
base_current_A = NaN*t_grid; 

for i=1:length(t_grid)
    relavent_i = abs(days_from_exp_start-t_grid(i)) < t_grid(2)-t_grid(1);
    
    if isempty(relavent_i)
        continue;
    end
    
    % Measure current by comparing the transition which LED switch is
    % switched on
    i_off_ONPART  =   when_is_state(states,'Off->day_shade_TransitionStep0') & relavent_i; %On
    i_sw_on =  when_is_state(states,'Off->day_shade_TransitionStep3') & relavent_i; %Off
    i_fr_on =  when_is_state(states,'Off->day_shade_TransitionStep4') & relavent_i; %Off
    i_all_on = when_is_state(states,'Off->day_shade_TransitionStep5') & relavent_i; %Off
    
    i_all_on2 = when_is_state(states,'day_shade->Off_TransitionStep0') & relavent_i; %Off
    
    if ~any(i_off_ONPART) || ~any(i_sw_on)
        led_sw_current_A(i) = NaN;
    else
        led_sw_current_A(i) = mean(INA260_Current_A(i_sw_on))-mean(INA260_Current_A(i_off_ONPART));
    end
    
    if ~any(i_sw_on) || ~any(i_fr_on)
        fr_current_A(i) = NaN;
    else
        fr_current_A(i) = mean(INA260_Current_A(i_fr_on))-mean(INA260_Current_A(i_sw_on));
    end
    
    if ~any(i_fr_on) || ~any(i_all_on)
        neopixel_current_A(i) = NaN;
    else
        neopixel_current_A(i) = mean(INA260_Current_A(i_all_on))-mean(INA260_Current_A(i_fr_on));
    end
    
   
    base_current_A(i) = mean([mean(INA260_Current_A(i_sw_on)),mean(INA260_Current_A(i_off_ONPART))]);
       
    
    mean(INA260_Current_A(i_all_on)) - mean(INA260_Current_A(i_all_on2))
end  

% LED current between consequence steps
plot(...
    t_grid,led_sw_current_A,'o',...
    t_grid,fr_current_A,'o',...
    t_grid,neopixel_current_A,'o')
legend('SW','fr','neopixel');
ylabel('Current [A]');

return;

%% Helper functions
function y = getdatetime(x)
try
    y = datenum(strtrim(x),'mm/dd/yyyy HH:MM:SS');
catch
    y = NaN;
end
end

function y = getscalarparameter(x)
try
    y = str2double(x);
catch
    y = NaN;
end
end

function y = isswon(x)
if strcmpi(x,'on')
    y = true;
else
    y = false;
end
end

function i = when_is_state(states,search_state)
i=cellfun(@(x)(strcmpi(x,search_state)), states);
i=boolean(i);
end
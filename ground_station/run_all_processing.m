% This script runs all processing for SpaceChickpeas

addpath(genpath('..\..\'));

%% Generate telemetry image

disp('ISS Telemetry Overview');
telemetry_csv_path_ = 'C:\_AvivLabs\ISSModule/02 Raw Telemetry/telematry.csv';
generate_telemetry_overview;

input('Press enter when done to move to Earth experiment telemetry');
telemetry_csv_path_ = 'C:\_AvivLabs/EarthControl/telematry.csv';
generate_telemetry_overview;

input('Press enter to continue');

%% Process medtronic images

% Convert
disp('');
disp('Navigate to');
disp('C:\_AvivLabs\ISSModule\03 Raw Images')
Hummus_Viewer;

% Move Bins
MoveBins;

%% Generate a video from root images
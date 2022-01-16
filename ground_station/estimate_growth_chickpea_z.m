%% Inputs
output_file_name = 'animated.gif';
base_input_folder = '..\images';

date_str = '22-01-14__23_40';

% Set camera l&r and focus setting
l_camera = 'CA_F0130';
r_camera = 'CC_F0130';

% Predefine points
if ~exist('anc_pt_l','var')
    anc_pt_l = [1200, 1200; 3400, 1100; 3400, 2100; 1200, 2000];
    anc_pt_r = [800 , 1100; 3000, 1100; 3000, 2000;  800, 2000];
    cp_pt_l  = [1550 1250 ; 1950, 1250; 2300, 1250; 2700, 1200; 1400, 1550; 1750, 1550; 2150, 1550; 2500, 1500; 2900, 1550; 1600, 1850; 1950, 1850; 2300, 1850; 2700, 1850; 3100, 1850];
    cp_pt_r  = [1300 1150 ; 1700, 1150; 2050, 1150; 2400, 1250; 1100, 1500; 1500, 1550; 1850, 1550; 2250, 1550; 2600, 1550; 1300, 1850; 1700, 1800; 2100, 1850; 2500, 1800; 2800, 1850];
end

%% Load Image
file_path_l = [base_input_folder '\' date_str '_' l_camera '.jpg'];
file_path_r = [base_input_folder '\' date_str '_' r_camera '.jpg'];
iml = imread(file_path_l);
imr = imread(file_path_r);

%% Mark ancore points & calibrate camera model
disp('Mark ancore points and close screen')
[anc_pt_l,anc_pt_r] = cpselect(iml,imr,anc_pt_l,anc_pt_r,'wait',true);

% Calibrate camera model. A is 3 by 5
%  x    = A *   ij
%             [i_l] 
% [x]         [j_l]
% [y]   = A * [i_r]
% [z]         [j_l]
%             [ 1 ]
x = [-1 1 1 -1; 0.5 0.5 0 0; 0 0 0 0]*95.5; %mm
ij = [anc_pt_l(:,1)'; anc_pt_l(:,2)'; anc_pt_r(:,1)'; anc_pt_r(:,2)'; ones(1,size(anc_pt_r,1))];

A_best = [];
e_best = Inf;
for i=1:100
    
    A = rand(3,5);
    %A(:,5) = 0; % ij=0 is at x=[0,0,0]
    A(2,1) = 0; % increasing i doesn't have any y component
    A(2,3) = 0; % increasing i doesn't have any y component
    A(1,2) = 0; % increasing j doesn't have any x component
    A(1,4) = 0; % increasing j doesn't have any x component
    a=1;
    options = optimset('MaxFunEvals',1e7);
    [A,e] = fminsearch(@(A)(sum(sum( (A*ij-x).^2))),A);
    
    if (e<e_best)
        A_best = A;
        e_best = e;
    end
end

[A_best] = fminsearch(@(A)(sum(sum( (A*ij-x).^2))),A_best);
[A_best] = fminsearch(@(A)(sum(sum( (A*ij-x).^2))),A_best);
A_best*ij


%% Mark growth
disp('Mark the Chickpeas');
[cp_pt_l,cp_pt_r] = cpselect(iml,imr,cp_pt_l,cp_pt_r,'wait',true);

ij = [cp_pt_l(:,1)'; cp_pt_l(:,2)'; cp_pt_r(:,1)'; cp_pt_r(:,2)'; ones(1,size(cp_pt_l,1))];
chickpea_pos = A*ij;

%% Plot results
t_Hr = 24*(time_picture_was_taken(file_path_l) - ...
    time_of_first_picture(base_input_folder));
figure(2);
imshow(iml);
for i=1:size(cp_pt_l,1)
    text(cp_pt_l(i,1),cp_pt_l(i,2),sprintf('%.1fmm',chickpea_pos(3,i)),'Color',[1 1 1]);
end
title(sprintf('%.1f Hours After Experiment Start',t_Hr));
xlabel('Shoot Height Above Gel Plane');
saveas(gcf,sprintf('%.1fHr.jpg',t_Hr));

return;

%%
%   y   = a *  x + b
% [i_l]       [x]
% [j_l] = A * [y]
% [i_r]       [z]
% [j_r]       [1]
y = [anc_pt_l(:,1)'; anc_pt_l(:,2)'; anc_pt_r(:,1)'; anc_pt_r(:,2)'];
x = [-2 2 2 -2; 1 1 0 0; 0 0 0 1; 1 1 1 1];

A = b * x^-1;
A_1 = A^-1;

A_1*[0;0;0;0]

%%
A_best = [];
e_best = Inf;
for i=1:100
    
    A = rand(4,4);
    [A,e] = fminsearch(@(A)(sum(sum( (A*x-b).^2))),A);
    
    if (e<e_best)
        A_best = A;
    end
end



return;
%%
[axisa, axisb] = show_image(iml,imr);

getp
%h = images.roi.Point(gca,'Position',[pt_l_0(1,1),pt_l_0(1,2)])


function [axisa, axisb] = show_image(iml,imr)
    h = figure(1);
    set(h,'units','normalized','outerposition',[0 0 1 1])
    subplot(1,6,1:3);
    imshow(iml);
    axisa = gca;
    subplot(1,6,4:6);
    imshow(imr);
    axisb = gca;
end
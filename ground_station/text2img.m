function im=text2img(txt,font_size)

%% Input checks
if ~exist('txt','var')
    txt = 'hello world';
end

if ~exist('font_size','var')
    font_size=10;
end

%% Get the image
f = figure;
text(0.5,0.5,txt,'FontSize',font_size)
frame = getframe(f); 
im = frame2im(frame);
close(f);

%% Remove all un-necessary parts
img = im2gray(im);

i2Delete1 = find(min(img,[],2)<10 & (1:size(img,1))'>0.1*size(img,1),1,'first');
i2Delete2 = find(min(img,[],2)<10 & (1:size(img,1))'<0.9*size(img,1),1,'last');
im([(1:i2Delete1-5) ((i2Delete2+5):end)],:,:) = [];

i2Delete1 = find(min(img,[],1)<10 & (1:size(img,2))>0.1*size(img,2),1,'first');
i2Delete2 = find(min(img,[],1)<10 & (1:size(img,2))<0.9*size(img,2),1,'last');
im(:,[(1:i2Delete1-5) ((i2Delete2+5):end)],:) = [];
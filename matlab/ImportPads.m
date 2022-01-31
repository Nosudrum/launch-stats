%% Preamble
clc
clear
close all

%% Import parameters
API="ll"; % ll or lldev
APIver="2.2.0";
APIkey=fileread('APIkey.txt');
options = weboptions;
options.Timeout=20;
options.HeaderFields=['Authorization',strcat("Token ",APIkey)];

%% Import Pads
FirstCall=webread(strcat("https://",API,".thespacedevs.com/",APIver,"/pad/?limit=100&mode=detailed"),options);
NbPads=FirstCall.count;
NbCalls=ceil(NbPads/100);
Pads=FirstCall.results;
nextURL=FirstCall.next;
ii=1;
disp(strcat("Total Pads :",num2str(NbPads)))
while ~isempty(nextURL)
    ii=ii+1;
    LoopCall=webread(nextURL,options);
    Pads = [Pads;LoopCall.results];
    nextURL=LoopCall.next;
    disp(strcat("API Call ",num2str(ii),"/",num2str(NbCalls)))
end

%% Export Pads Struct
save("data/Pads.mat","Pads")
disp("Successfully exported Pads to file.")
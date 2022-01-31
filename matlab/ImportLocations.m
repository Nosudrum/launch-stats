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

%% Import Locations
FirstCall=webread(strcat("https://",API,".thespacedevs.com/",APIver,"/location/?limit=100&mode=detailed"),options);
NbLocs=FirstCall.count;
NbCalls=ceil(NbLocs/100);
Locs=FirstCall.results;
nextURL=FirstCall.next;
ii=1;
disp(strcat("Total Locations :",num2str(NbLocs)))
while ~isempty(nextURL)
    ii=ii+1;
    LoopCall=webread(nextURL,options);
    Locs = [Locs;LoopCall.results];
    nextURL=LoopCall.next;
    disp(strcat("API Call ",num2str(ii),"/",num2str(NbCalls)))
end

%% Export Locations Struct
save("data/Locations.mat","Locs")
disp("Successfully exported Locations to file.")
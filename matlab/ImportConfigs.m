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

%% Import Orbits
FirstCall=webread(strcat("https://",API,".thespacedevs.com/",APIver,"/config/orbit/?limit=100&mode=detailed"),options);
NbOrbits=FirstCall.count;
NbCalls=ceil(NbOrbits/100);
Orbits=FirstCall.results;
nextURL=FirstCall.next;
ii=1;
disp(strcat("Total Orbits :",num2str(NbOrbits)))
while ~isempty(nextURL)
    ii=ii+1;
    LoopCall=webread(nextURL,options);
    Orbits = [Orbits;LoopCall.results];
    nextURL=LoopCall.next;
    disp(strcat("API Call ",num2str(ii),"/",num2str(NbCalls)))
end

%% Export Orbits Struct
save("data/Orbits.mat","Orbits")
disp("Successfully exported Orbits to file.")

%% Import Statuses
FirstCall=webread(strcat("https://",API,".thespacedevs.com/",APIver,"/config/launchstatus/?limit=100&mode=detailed"),options);
NbStatuses=FirstCall.count;
NbCalls=ceil(NbOrbits/100);
Statuses=FirstCall.results;
nextURL=FirstCall.next;
ii=1;
disp(strcat("Total Statuses :",num2str(NbStatuses)))
while ~isempty(nextURL)
    ii=ii+1;
    LoopCall=webread(nextURL,options);
    Statuses = [Statuses;LoopCall.results];
    nextURL=LoopCall.next;
    disp(strcat("API Call ",num2str(ii),"/",num2str(NbCalls)))
end

%% Export Statuses Struct
save("Statuses.mat","Statuses")
disp("Successfully exported Statuses to file.")
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

%% Import launches
FirstCall=webread(strcat("https://",API,".thespacedevs.com/",APIver,"/launch/?limit=100"),options);
NbLaunches=FirstCall.count;
NbCalls=ceil(NbLaunches/100);
Launches=FirstCall.results;
nextURL=FirstCall.next;
ii=1;
disp(strcat("Total Launches :",num2str(NbLaunches)))
while ~isempty(nextURL)
    ii=ii+1;
    LoopCall=webread(nextURL,options);
    Launches = [Launches;LoopCall.results];
    nextURL=LoopCall.next;
    disp(strcat("API Call ",num2str(ii),"/",num2str(NbCalls)))
end

%% Export Launches Struct
save("data/Launches.mat","Launches")
disp("Successfully exported Launches to file.")
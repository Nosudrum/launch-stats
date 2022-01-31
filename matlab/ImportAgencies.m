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

%% Import Agencies
FirstCall=webread(strcat("https://",API,".thespacedevs.com/",APIver,"/agencies/?limit=100"),options);
NbAgencies=FirstCall.count;
NbCalls=ceil(NbAgencies/100);
Agencies=FirstCall.results;
nextURL=FirstCall.next;
ii=1;
disp(strcat("Total Agencies :",num2str(NbAgencies)))
while ~isempty(nextURL)
    ii=ii+1;
    LoopCall=webread(nextURL,options);
    Agencies = [Agencies;LoopCall.results];
    nextURL=LoopCall.next;
    disp(strcat("API Call ",num2str(ii),"/",num2str(NbCalls)))
end

%% Export Agencies Struct
save("data/Agencies.mat","Agencies")
disp("Successfully exported Agencies to file.")
%% Preamble
clc
clear
close all

%% Import parameters
API="ll"; % ll or lldev
APIver="2.2.0";
APIkey="e130e1a3826c13b927fb47590096f9f2dcb52ec5";
options = weboptions;
options.Timeout=20;
options.HeaderFields=['Authorization',strcat("Token ",APIkey)];

%% Import LauncherConfigs
FirstCall=webread(strcat("https://",API,".thespacedevs.com/",APIver,"/config/launcher/?limit=100&mode=detailed"),options);
NbLC=FirstCall.count;
NbCalls=ceil(NbLC/100);
LCs=FirstCall.results;
nextURL=FirstCall.next;
ii=1;
disp(strcat("Total LauncherConfigs :",num2str(NbLC)))
while ~isempty(nextURL)
    ii=ii+1;
    LoopCall=webread(nextURL,options);
    LCs = [LCs;LoopCall.results];
    nextURL=LoopCall.next;
    disp(strcat("API Call ",num2str(ii),"/",num2str(NbCalls)))
end

%% Isolate LCs with non-null launch cost
jj=0;
for ii=1:length(LCs)
    if ~isempty(LCs(ii).launch_cost)
        jj=jj+1;
        LCName(jj)=string(LCs(ii).name);
        LCid(jj)=LCs(ii).id;
        LCcost(jj)=string(LCs(ii).launch_cost);
    end
end
















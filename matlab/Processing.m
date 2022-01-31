%% Preamble
clc
clear
close all

%% Plot figures
plotFigs=true;

%% Import Data
load("Launches.mat")
load("Agencies.mat")
load("Pads.mat")
load("Locations.mat")
load("Orbits.mat")
load("Statuses.mat")

%% Launches Data
LaunchName=strings(1,length(Launches));
LaunchStatus=NaN(1,length(Launches));
LaunchT0=NaT(1,length(Launches));
LaunchLSP=NaN(1,length(Launches));
LaunchCountry=strings(1,length(Launches));
LaunchOrbit=NaN(1,length(Launches));
LaunchPad=NaN(1,length(Launches));
LaunchProgram=NaN(1,length(Launches));

for ii=1:length(Launches)
    LaunchName(ii)=string(Launches(ii).name);
    LaunchStatus(ii)=Launches(ii).status.id;
    LaunchT0(ii)=datetime(Launches(ii).net,'Format','yyyy-MM-dd''T''HH:mm:ss''Z''');
    LaunchLSP(ii)=Launches(ii).launch_service_provider.id;
    LaunchCountry(ii)=Launches(ii).pad.location.country_code;
    if ~isempty(Launches(ii).mission)
        if ~isempty(Launches(ii).mission.orbit)
            LaunchOrbit(ii)=Launches(ii).mission.orbit.id;
        end
    end
    LaunchPad(ii)=Launches(ii).pad.id;
    if ~isempty(Launches(ii).program)
        LaunchProgram(ii)=Launches(ii).program.id;
    end 
end
% LaunchTable=table(LaunchName',LaunchStatus',LaunchT0',LaunchLSP',LaunchPad',LaunchOrbit',LaunchProgram');
% LaunchTable.Properties.VariableNames = {'Name','Status','T-0','LSP','Pad','Orbit','Program'};
% LaunchT0<datetime('now')

%% Locations table
jj=0;
for ii=1:length(Locs)
    if isempty(Locs(ii).pads)
        continue
    end
    jj=jj+1;
    LocsName(jj)=string(Locs(ii).name);
    LocsLat(jj)=str2double(Locs(ii).pads(1).latitude);
    LocsLong(jj)=str2double(Locs(ii).pads(1).longitude);
    LocsCount(jj)=Locs(ii).total_launch_count;
end
%% Locations Map
if ~plotFigs
    return
end

%% Figures

% Location Map
figure
geobubble(LocsLat,LocsLong,LocsCount,'BubbleColorList',[1 0 0])
geobasemap('satellite')

% Launch attemps per launch country
figure
[N1,edges] = histcounts(year(LaunchT0((LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='RUS' | LaunchCountry=='KAZ')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
[N2,edges] = histcounts(year(LaunchT0((LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='USA')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
[N3,edges] = histcounts(year(LaunchT0((LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='CHN')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
[N4,edges] = histcounts(year(LaunchT0((LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry~='USA' & LaunchCountry~='RUS' & LaunchCountry~='KAZ' & LaunchCountry~='CHN')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
bar(edges(1:(end-1)),[N1',N2',N3',N4'],'stacked')
legend("USSR/Russia","USA","China","Others",'Location','southoutside','Orientation','horizontal')
title('Orbital launch attempts per launch country since 1957')
ylim([0 150])

% Successful orbital launches per launch country
figure
[N1,edges] = histcounts(year(LaunchT0((LaunchStatus==3).*(LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='RUS' | LaunchCountry=='KAZ')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
[N2,edges] = histcounts(year(LaunchT0((LaunchStatus==3).*(LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='USA')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
[N3,edges] = histcounts(year(LaunchT0((LaunchStatus==3).*(LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='CHN')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
[N4,edges] = histcounts(year(LaunchT0((LaunchStatus==3).*(LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry~='USA' & LaunchCountry~='RUS' & LaunchCountry~='KAZ' & LaunchCountry~='CHN')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
bar(edges(1:(end-1)),[N1',N2',N3',N4'],'stacked')
legend("Russia & Kazakhstan","USA","China","Others",'Location','southoutside','Orientation','horizontal')
title('Successful orbital launches per launch country since 1957')

% Graph of successful orbital launches per launch country
% figure
% plot(edges(1:(end-1)),[N1',N2',N3',N4'])
% legend("Russia & Kazakhstan","USA","China","Others",'Location','southoutside','Orientation','horizontal')
% set(gcf, 'InvertHardCopy', 'off'); 
% set(gcf,'Color',[0 0 0]);
% set(gcf,'Position',[0,0,1920,1080])
% saveas(gcf,'Barchart.png')
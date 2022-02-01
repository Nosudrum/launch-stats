# Preamble
import requests
import math
import json

# Import parameters
API = 'll'  # ll or lldev
API_ver = '2.2.0'
file = open('APIkey.txt', 'r')
API_key = file.read()
file.close()
headers_dict = {'Authorization': 'Token ' + API_key}

# Import Orbits
API_url = 'https://' + API + '.thespacedevs.com/' + API_ver + '/config/orbit/?limit=100&mode=detailed'
FirstCall = requests.get(API_url, headers=headers_dict, timeout=20).json()
NbOrbits = FirstCall['count']
NbCalls = math.ceil(NbOrbits / 100.0)
Orbits = FirstCall['results']
nextURL = FirstCall['next']
ii = 1
print('Total Orbits : ' + str(NbOrbits))
print('API Call ' + str(ii) + '/' + str(NbCalls))
while nextURL is not None:
    ii += 1
    LoopCall = requests.get(nextURL, headers=headers_dict, timeout=20).json()
    Orbits.update(LoopCall['results'])
    nextURL = LoopCall['next']
    print('API Call ' + str(ii) + '/' + str(NbCalls))

# Export Orbits Dictionary
with open('data/Orbits.json', 'w+') as f:
    json.dump(Orbits, f, indent=4)
print('Successfully exported Orbits to file.')

# # Import Statuses
# FirstCall = webread(
#     strcat("https://", API, ".thespacedevs.com/", APIver, "/config/launchstatus/?limit=100&mode=detailed"), options);
# NbStatuses = FirstCall.count;
# NbCalls = ceil(NbOrbits / 100);
# Statuses = FirstCall.results;
# nextURL = FirstCall.next;
# ii = 1;
# disp(strcat("Total Statuses :", num2str(NbStatuses)))
# while ~isempty(nextURL)
#     ii = ii + 1;
#     LoopCall = webread(nextURL, options);
#     Statuses = [Statuses;
#     LoopCall.results];
#     nextURL = LoopCall.next;
#     disp(strcat("API Call ", num2str(ii), "/", num2str(NbCalls)))
# end
#
# # Export Statuses Struct
# save("Statuses.mat", "Statuses")
# disp("Successfully exported Statuses to file.")

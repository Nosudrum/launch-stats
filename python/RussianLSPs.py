from playground import LaunchLSP, LaunchPad

# Code used to check consistency and coherence of LSP assignments to Soviet & Russian launches

Location_ID = {'Plesetsk': 6, 'Baikonur': 15, 'Dombarovskiy': 5, 'Kapustin Yar': 30, 'Svobodny': 146, 'Vostochny': 18}

LSPs_Plesetsk = LaunchLSP[LaunchPad["location.id"] == Location_ID["Plesetsk"]]["name"].unique()
LSPs_Baikonur = LaunchLSP[LaunchPad["location.id"] == Location_ID["Baikonur"]]["name"].unique()
LSPs_Dombarovskiy = LaunchLSP[LaunchPad["location.id"] == Location_ID["Dombarovskiy"]]["name"].unique()
LSPs_KapustinYar = LaunchLSP[LaunchPad["location.id"] == Location_ID["Kapustin Yar"]]["name"].unique()
LSPs_Svobodny = LaunchLSP[LaunchPad["location.id"] == Location_ID["Svobodny"]]["name"].unique()
LSPs_Vostochny = LaunchLSP[LaunchPad["location.id"] == Location_ID["Vostochny"]]["name"].unique()


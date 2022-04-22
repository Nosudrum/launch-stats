from Processing import PastLSPs, PastT0s, Agencies, PastName
from pandas import DataFrame, concat

BestDelta = DataFrame(columns=['LSP_name', 'TimeDelta', 'T1', 'Name1', 'T2', 'Name2'])
for LSP in PastLSPs["id"].unique().tolist():
    if PastT0s[PastLSPs["id"] == LSP].size <= 1:
        continue
    LSP_T0s = PastT0s[PastLSPs["id"] == LSP].copy()
    LSP_TimeDelta = LSP_T0s.diff()

    minDelta = LSP_TimeDelta.min().item()
    idx_minDelta = LSP_TimeDelta.idxmin()
    T2 = LSP_T0s.loc[idx_minDelta].net.item()
    Name2 = PastName[PastLSPs["id"] == LSP].loc[idx_minDelta].name.item()
    T1 = LSP_T0s.shift(1).loc[idx_minDelta].net.item()
    Name1 = PastName[PastLSPs["id"] == LSP].shift(1).loc[idx_minDelta].name.item()
    LSP_dict = {'LSP_name': Agencies[Agencies["id"] == LSP]["name"].values[0], 'TimeDelta': minDelta,
                'T1': T1, 'Name1': Name1, 'T2': T2, 'Name2': Name2}

    BestDelta = concat([BestDelta, DataFrame(LSP_dict, index=[LSP])])
BestDelta.sort_values("TimeDelta").to_clipboard()

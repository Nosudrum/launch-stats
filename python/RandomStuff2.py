from Processing import PastLSPs, PastT0s, Agencies, PastName
from pandas import DataFrame, concat

# LSP_BestDelta = DataFrame(columns=['LSP_name', 'TimeDelta', 'T1', 'Name1', 'T2', 'Name2'])
# for LSP in PastLSPs["id"].unique().tolist():
#     if PastT0s[PastLSPs["id"] == LSP].size <= 1:
#         continue
#     LSP_T0s = PastT0s[PastLSPs["id"] == LSP].copy()
#     LSP_TimeDelta = LSP_T0s.diff()
#
#     minDelta = LSP_TimeDelta.min().item()
#     idx_minDelta = LSP_TimeDelta.idxmin()
#     T2 = LSP_T0s.loc[idx_minDelta].net.item()
#     Name2 = PastName[PastLSPs["id"] == LSP].loc[idx_minDelta].name.item()
#     T1 = LSP_T0s.shift(1).loc[idx_minDelta].net.item()
#     Name1 = PastName[PastLSPs["id"] == LSP].shift(1).loc[idx_minDelta].name.item()
#     LSP_dict = {'LSP_name': Agencies[Agencies["id"] == LSP]["name"].values[0], 'TimeDelta': minDelta,
#                 'T1': T1, 'Name1': Name1, 'T2': T2, 'Name2': Name2}
#
#     LSP_BestDelta = concat([LSP_BestDelta, DataFrame(LSP_dict, index=[LSP])])
# LSP_BestDelta.sort_values("TimeDelta").to_clipboard()

BestDelta = DataFrame(
    {"TimeDelta": PastT0s.copy().diff().net, "Name1": PastName.copy().shift(1).name, "T1": PastT0s.copy().shift(1).net,
     "Name2": PastName.copy().name, "T2": PastT0s.copy().net})
BestDelta.sort_values("TimeDelta").to_clipboard()

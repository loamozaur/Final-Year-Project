import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 500) # max columns displayed is expanded to 500


def main():
    # column names to be read
    colnames = []
    for i in range(4):
        for j in range(1, 13):
            colnames.append(str(i) + 'VOEM' + str(j))

    data = pd.read_csv('sumo.csv', usecols=colnames, header=0)

    # Calculates connection movements and overflows
    data['0con1'] = data['0VOEM3'] + data['0VOEM7'] + data['0VOEM11']
    data['0con1check'] = data['1VOEM11'] + data['1VOEM12']
    data['0con2'] = data['1VOEM1'] + data['1VOEM5']
    data['0con2check'] = data['0VOEM4'] + data['0VOEM5'] + data['0VOEM6']

    data['2con1'] = data['2VOEM3'] + data['2VOEM7'] + data['2VOEM11']
    data['2con1check'] = data['3VOEM11'] + data['3VOEM12']
    data['2con2'] = data['3VOEM1'] + data['3VOEM5']
    data['2con2check'] = data['2VOEM4'] + data['2VOEM5'] + data['2VOEM6']

    data['1con1'] = data['1VOEM3'] + data['1VOEM11']
    data['1con1check'] = data['2VOEM10'] + data['2VOEM11'] + data['2VOEM12']
    data['1con2'] = data['2VOEM1'] + data['2VOEM5'] + data['2VOEM9']
    data['1con2check'] = data['1VOEM4'] + data['1VOEM5']

    # testing if the calculations right
    cond0 = (data['0con1'] == data['0con1check']) & (data['0con2'] == data['0con2check'])
    cond1 = (data['1con1'] == data['1con1check']) & (data['1con2'] == data['1con2check'])
    cond2 = (data['2con1'] == data['2con1check']) & (data['2con2'] == data['2con2check'])
    # final test: true means no problems, false means error
    data['check-1'] = cond0 & cond1 & cond2

    # Calculating distribution factors
    # Connection 1
    data['0con1_dist1'] = data['0VOEM3'] / data['0con1']
    data['0con1_dist3'] = data['0VOEM7'] / data['0con1']
    data['0con1_dist4'] = data['0VOEM11'] / data['0con1']
    data['0con2_dist1'] = data['1VOEM1'] / data['0con2']
    data['0con2_dist2'] = data['1VOEM5'] / data['0con2']

    # Connection 2
    data['1con1_dist1'] = data['1VOEM3'] / data['1con1']
    data['1con1_dist4'] = data['1VOEM11'] / data['1con1']
    data['1con2_dist1'] = data['2VOEM1'] / data['1con2']
    data['1con2_dist2'] = data['2VOEM5'] / data['1con2']
    data['1con2_dist3'] = data['2VOEM9'] / data['1con2']

    # Connection 3
    data['2con1_dist1'] = data['2VOEM3'] / data['2con1']
    data['2con1_dist3'] = data['2VOEM7'] / data['2con1']
    data['2con1_dist4'] = data['2VOEM11'] / data['2con1']
    data['2con2_dist1'] = data['3VOEM1'] / data['2con2']
    data['2con2_dist2'] = data['3VOEM5'] / data['2con2']

    # testing if the calculations right
    cond1 = (0.999 < (data['0con1_dist1'] + data['0con1_dist3'] + data['0con1_dist4'])) & (
                0.999 < (data['0con2_dist1'] + data['0con2_dist2'])) & (
                        (data['0con1_dist1'] + data['0con1_dist3'] + data['0con1_dist4']) < 1.001) & (
                        (data['0con2_dist1'] + data['0con2_dist2']) < 1.001)
    cond2 = (0.999 < (data['1con1_dist1'] + data['1con1_dist4'])) & (
                0.999 < (data['1con2_dist1'] + data['1con2_dist2'] + data['1con2_dist3'])) & (
                        (data['1con1_dist1'] + data['1con1_dist4']) < 1.001) & (
                        (data['1con2_dist1'] + data['1con2_dist2'] + data['1con2_dist3']) < 1.001)
    cond3 = (0.999 < (data['2con1_dist1'] + data['2con1_dist3'] + data['2con1_dist4'])) & (
                0.999 < (data['2con2_dist1'] + data['2con2_dist2'])) & (
                        (data['2con1_dist1'] + data['2con1_dist3'] + data['2con1_dist4']) < 1.001) & (
                        (data['2con2_dist1'] + data['2con2_dist2']) < 1.001)
    cond = cond1 & cond2 & cond3
    data['check-2'] = cond  # indicates if the s

        # relation from intersection to intersection:
        # from intersection 1 with 3 independent legs
    data['1to2_dist1'] = data['0con1_dist1']
    data['1to2_dist3'] = data['0con1_dist3']
    data['1to2_dist4'] = data['0con1_dist4']
    data['1to3_dist1'] = data['0con1_dist1'] * data['1con1_dist4']
    data['1to3_dist3'] = data['0con1_dist3'] * data['1con1_dist4']
    data['1to3_dist4'] = data['0con1_dist4'] * data['1con1_dist4']
    data['1to4_dist1'] = data['0con1_dist1'] * data['1con1_dist4'] * data['2con1_dist4']
    data['1to4_dist3'] = data['0con1_dist3'] * data['1con1_dist4'] * data['2con1_dist4']
    data['1to4_dist4'] = data['0con1_dist4'] * data['1con1_dist4'] * data['2con1_dist4']

    # from intersection 2 with 1 independent leg
    data['2to1_dist1'] = data['0con2_dist1']
    data['2to3_dist1'] = data['1con1_dist1']
    data['2to4_dist1'] = data['1con1_dist1'] * data['2con1_dist4']

    # from intersection 3 with 2 independent legs
    data['3to2_dist1'] = data['1con2_dist1']
    data['3to2_dist3'] = data['1con2_dist3']
    data['3to4_dist1'] = data['2con1_dist1']
    data['3to4_dist3'] = data['2con1_dist3']
    data['3to1_dist1'] = data['1con2_dist1'] * data['0con2_dist2']
    data['3to1_dist3'] = data['1con2_dist3'] * data['0con2_dist2']

    # from intersection 4 with 2 independent legs
    data['4to3_dist1'] = data['2con2_dist1']
    data['4to3_dist2'] = data['2con2_dist2']
    data['4to2_dist1'] = data['2con2_dist1'] * data['1con2_dist2']
    data['4to2_dist2'] = data['2con2_dist2'] * data['1con2_dist2']
    data['4to1_dist1'] = data['2con2_dist1'] * data['1con2_dist2'] * data['0con2_dist2']
    data['4to1_dist2'] = data['2con2_dist2'] * data['1con2_dist2'] * data['0con2_dist2']

    # Calculating OD data with non-rounded values
    # for the same intersection
    data['1to2'] = (data['0VOEM12']).astype('int32') + 1
    data['1to8'] = (data['0VOEM10']).astype('int32') + 1
    data['2to1'] = (data['0VOEM1']).astype('int32') + 1
    data['2to8'] = (data['0VOEM2']).astype('int32') + 1
    data['8to1'] = (data['0VOEM9']).astype('int32') + 1
    data['8to2'] = (data['0VOEM8']).astype('int32') + 1
    data['4to7'] = (data['2VOEM2']).astype('int32') + 1
    data['7to4'] = (data['2VOEM8']).astype('int32') + 1
    data['5to6'] = (data['3VOEM3']).astype('int32') + 1
    data['6to5'] = (data['3VOEM4']).astype('int32') + 1

    # for distance of 1 connection
    data['2to3'] = (data['1VOEM12'] * data['1to2_dist1']).astype('int32') + 1
    data['8to3'] = (data['1VOEM12'] * data['1to2_dist3']).astype('int32') + 1
    data['1to3'] = (data['1VOEM12'] * data['1to2_dist4']).astype('int32') + 1
    data['3to2'] = (data['0VOEM4'] * data['2to1_dist1']).astype('int32') + 1
    data['3to1'] = (data['0VOEM5'] * data['2to1_dist1']).astype('int32') + 1
    data['3to8'] = (data['0VOEM6'] * data['2to1_dist1']).astype('int32') + 1
    data['3to4'] = (data['2VOEM12'] * data['2to3_dist1']).astype('int32') + 1
    data['3to7'] = (data['2VOEM10'] * data['2to3_dist1']).astype('int32') + 1
    data['4to3'] = (data['1VOEM4'] * data['3to2_dist1']).astype('int32') + 1
    data['7to3'] = (data['1VOEM4'] * data['3to2_dist3']).astype('int32') + 1
    data['4to5'] = (data['3VOEM12'] * data['3to4_dist1']).astype('int32') + 1
    data['4to6'] = (data['3VOEM11'] * data['3to4_dist1']).astype('int32') + 1
    data['7to5'] = (data['3VOEM12'] * data['3to4_dist3']).astype('int32') + 1
    data['7to6'] = (data['3VOEM11'] * data['3to4_dist3']).astype('int32') + 1
    data['5to4'] = (data['2VOEM4'] * data['4to3_dist1']).astype('int32') + 1
    data['5to7'] = (data['2VOEM6'] * data['4to3_dist1']).astype('int32') + 1
    data['6to4'] = (data['2VOEM4'] * data['4to3_dist2']).astype('int32') + 1
    data['6to7'] = (data['2VOEM6'] * data['4to3_dist2']).astype('int32') + 1

    # for distance of 2 connections
    data['2to4'] = (data['2VOEM12'] * data['1to3_dist1']).astype('int32') + 1
    data['2to7'] = (data['2VOEM10'] * data['1to3_dist1']).astype('int32') + 1
    data['1to4'] = (data['2VOEM12'] * data['1to3_dist4']).astype('int32') + 1
    data['1to7'] = (data['2VOEM10'] * data['1to3_dist4']).astype('int32') + 1
    data['8to4'] = (data['2VOEM12'] * data['1to3_dist3']).astype('int32') + 1
    data['8to7'] = (data['2VOEM10'] * data['1to3_dist3']).astype('int32') + 1
    data['3to5'] = (data['3VOEM12'] * data['2to4_dist1']).astype('int32') + 1
    data['3to6'] = (data['3VOEM11'] * data['2to4_dist1']).astype('int32') + 1
    data['4to1'] = (data['0VOEM5'] * data['3to1_dist1']).astype('int32') + 1
    data['4to2'] = (data['0VOEM4'] * data['3to1_dist1']).astype('int32') + 1
    data['4to8'] = (data['0VOEM6'] * data['3to1_dist1']).astype('int32') + 1
    data['7to1'] = (data['0VOEM5'] * data['3to1_dist3']).astype('int32') + 1
    data['7to2'] = (data['0VOEM4'] * data['3to1_dist3']).astype('int32') + 1
    data['7to8'] = (data['0VOEM6'] * data['3to1_dist3']).astype('int32') + 1
    data['5to3'] = (data['1VOEM4'] * data['4to1_dist1']).astype('int32') + 1
    data['6to3'] = (data['1VOEM4'] * data['4to1_dist2']).astype('int32') + 1

    # for distance of 3 connections
    data['1to5'] = (data['3VOEM12'] * data['1to4_dist4']).astype('int32') + 1
    data['1to6'] = (data['3VOEM11'] * data['1to4_dist4']).astype('int32') + 1
    data['2to5'] = (data['3VOEM12'] * data['1to4_dist1']).astype('int32') + 1
    data['2to6'] = (data['3VOEM11'] * data['1to4_dist1']).astype('int32') + 1
    data['8to5'] = (data['3VOEM12'] * data['1to4_dist3']).astype('int32') + 1
    data['8to6'] = (data['3VOEM11'] * data['1to4_dist3']).astype('int32') + 1
    data['5to1'] = (data['0VOEM5'] * data['4to1_dist1']).astype('int32') + 1
    data['6to1'] = (data['0VOEM5'] * data['4to1_dist2']).astype('int32') + 1
    data['5to2'] = (data['0VOEM4'] * data['4to1_dist1']).astype('int32') + 1
    data['6to2'] = (data['0VOEM4'] * data['4to1_dist2']).astype('int32') + 1
    data['5to8'] = (data['0VOEM6'] * data['4to1_dist1']).astype('int32') + 1
    data['6to8'] = (data['0VOEM6'] * data['4to1_dist2']).astype('int32') + 1

    ODpoints = ['1', '2', '3', '4', '5', '6', '7', '8']
    ODmatrix = pd.DataFrame(data=0, index=ODpoints, columns=ODpoints)

    newcolnames = pd.DataFrame()
    for i in range(4):
        for j in range(1, 13):
            name = str(i) + 'VOEM' + str(j) + 'n'
            newcolnames[name] = np.nan

    data = pd.concat([data, newcolnames], axis=1)

    for num in range(0, 1):
        for row in ODpoints:
            for col in ODpoints:
                if col != row: ODmatrix.loc[str(row)][str(col)] = data.iloc[num][str(row) + 'to' + str(col)]
        ODmat = ODmatrix.apply(lambda x: x + 1)
        n = num
        data.at[n, '0VOEM1n'] = ODmat.loc['2', '1']
        data.at[n, '0VOEM2n'] = ODmat.loc['2', '8']
        data.at[n, '0VOEM3n'] = ODmat.loc['2', '3':'7'].sum()
        data.at[n, '0VOEM4n'] = ODmat.loc['3':'7', '2'].sum()
        data.at[n, '0VOEM5n'] = ODmat.loc['3':'7', '1'].sum()
        data.at[n, '0VOEM6n'] = ODmat.loc['3':'7', '8'].sum()
        data.at[n, '0VOEM7n'] = ODmat.loc['8', '3':'7'].sum()
        data.at[n, '0VOEM8n'] = ODmat.loc['8', '2']
        data.at[n, '0VOEM9n'] = ODmat.loc['8', '1']
        data.at[n, '0VOEM10n'] = ODmat.loc['1', '8']
        data.at[n, '0VOEM11n'] = ODmat.loc['1', '3':'7'].sum()
        data.at[n, '0VOEM12n'] = ODmat.loc['1', '2']

        data.at[n, '1VOEM1n'] = ODmat.loc['3', ['1', '2', '8']].sum()
        data.at[n, '1VOEM2n'] = 0
        data.at[n, '1VOEM3n'] = ODmat.loc['3', '4':'7'].sum()
        data.at[n, '1VOEM4n'] = ODmat.loc[['4', '5', '6', '7'], '3'].sum()
        data.at[n, '1VOEM5n'] = ODmat.loc[['4', '5', '6', '7'], ['1', '2', '8']].sum().sum()
        data.at[n, '1VOEM6n'] = 0
        data.at[n, '1VOEM7n'] = 0
        data.at[n, '1VOEM8n'] = 0
        data.at[n, '1VOEM9n'] = 0
        data.at[n, '1VOEM10n'] = 0
        data.at[n, '1VOEM11n'] = ODmat.loc[['1', '2', '8'], '4':'7'].sum().sum()
        data.at[n, '1VOEM12n'] = ODmat.loc[['1', '2', '8'], '3'].sum()

        data.at[n, '2VOEM1n'] = ODmat.loc['4', ['1', '2', '3', '8']].sum()
        data.at[n, '2VOEM2n'] = ODmat.loc['4', '7']
        data.at[n, '2VOEM3n'] = ODmat.loc['4', ['5', '6']].sum()
        data.at[n, '2VOEM4n'] = ODmat.loc[['5', '6'], '4'].sum()
        data.at[n, '2VOEM5n'] = ODmat.loc[['5', '6'], ['1', '2', '3', '8']].sum().sum()
        data.at[n, '2VOEM6n'] = ODmat.loc[['5', '6'], '7'].sum()
        data.at[n, '2VOEM7n'] = ODmat.loc['7', ['5', '6']].sum()
        data.at[n, '2VOEM8n'] = ODmat.loc['7', '4']
        data.at[n, '2VOEM9n'] = ODmat.loc['7', ['1', '2', '3', '8']].sum()
        data.at[n, '2VOEM10n'] = ODmat.loc[['1', '2', '3', '8'], '7'].sum()
        data.at[n, '2VOEM11n'] = ODmat.loc[['1', '2', '3', '8'], ['5', '6']].sum().sum()
        data.at[n, '2VOEM12n'] = ODmat.loc[['1', '2', '3', '8'], '4'].sum()

        data.at[n, '3VOEM1n'] = ODmat.loc['5', ['1', '2', '3', '4', '7', '8']].sum()
        data.at[n, '3VOEM2n'] = 0
        data.at[n, '3VOEM3n'] = ODmat.loc['5', '6']
        data.at[n, '3VOEM4n'] = ODmat.loc['6', '5']
        data.at[n, '3VOEM5n'] = ODmat.loc['6', ['1', '2', '3', '4', '7', '8']].sum()
        data.at[n, '3VOEM6n'] = 0
        data.at[n, '3VOEM7n'] = 0
        data.at[n, '3VOEM8n'] = 0
        data.at[n, '3VOEM9n'] = 0
        data.at[n, '3VOEM10n'] = 0
        data.at[n, '3VOEM11n'] = ODmat.loc[['1', '2', '3', '4', '7', '8'], '6'].sum()
        data.at[n, '3VOEM12n'] = ODmat.loc[['1', '2', '3', '4', '7', '8'], '5'].sum()

    for site in range(4):
        for mov in range(1, 13):
            name1 = str(site) + 'VOEM' + str(mov)
            name2 = str(site) + 'VOEM' + str(mov) + 'n'
            name3 = 'check-' + str(site) + '-' + str(mov)
            data[name3] = data[name1] - data[name2]

    data.to_csv('outputfile.csv')

if __name__ == '__main__':
    main()
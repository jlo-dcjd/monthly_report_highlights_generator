import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import math


fy22 = [('OCT 2021'), ('NOV 2021'), ('DEC 2021'), ('JAN 2022'), ('FEB 2022'), ('MAR 2022'), ('APR 2022'), ('MAY 2022'),
       ('JUN 2022'), ('JUL 2022'), ('AUG 2022'), ('SEP 2022')]

st.title("Monthly Report Generator")

current = fy22[datetime.now().month + 1]
previous = fy22[datetime.now().month ]

month = st.radio(
     "Select month for the report:",
     ('Latest Month ({})'.format(current), 'Previous Month ({})'.format(previous)))
       
if month == 'Latest Month ({})'.format(current):
    current_month_fy = datetime.now().month + 1
    prev_month_fy = datetime.now().month
    st.write('You selected: report month ({}), previous month ({})'. format(fy22[current_month_fy], fy22[prev_month_fy]))
else:
    current_month_fy = datetime.now().month
    prev_month_fy = datetime.now().month - 1
    st.write('You selected: report month ({}), previous month ({})'. format(fy22[current_month_fy], fy22[prev_month_fy]))


uploaded_file = st.file_uploader("Upload a monthly report")
if uploaded_file is not None:
    
    # referrals
    df = pd.read_excel(uploaded_file, sheet_name=0, skiprows=7, usecols=list(range(1, 17))).T
    df.columns = df.iloc[0]
    df = df.iloc[2:, :np.where(df.iloc[0] == 'Total All Referrals')[0][0]+1]
    st.write(df)

    # Formalized Referrals
    col = ['Month', 'F Violent', 'F Property', 'F Drugs', 'F Weapons', 'F Other', 'M Violent',
       'M Property', 'M Drugs', 'M Weapons', 'M Other', 'O VOP', 'O Status',
       'O CINS Other than Status', 'O Other', 'Total Formalized Referrals']

    df2 = pd.read_excel(uploaded_file, sheet_name=0, usecols=list(range(1, 17))).T

    df2 = df2.iloc[2:, np.where(df2.iloc[0] == 'Formalized Referrals')[0][0]+1: np.where(df2.iloc[0] == 'Total Formalized Referrals')[0][1]+1]
    df2.columns = col
    df2 = df2.set_index('Month')
       
    # monthly court hearings
    df3 = pd.read_excel(uploaded_file, sheet_name=1, skiprows=6, usecols=list(range(1, 17))).T

    header = df3.iloc[:2]
    df3 = df3.iloc[2:, :np.where(header.values[0] == 'Total Held Hearings')[0][0] + 1]

    hearing_col = header.values[1][:np.where(header.values[1] == 'Total Held Certification Hearings')[0][0] + 1]
    df3.columns = np.append(hearing_col, np.where(header.values[0] == 'Total Held Hearings')[0][0] + 1)

    # replace all zeros w/ null
    df3 = df3.replace(0, np.nan)

    # hearing reset percent
    df4 = pd.read_excel(uploaded_file, sheet_name=1, skiprows=1, usecols=list(range(1, 17))).T

    header = df4.iloc[:2, :]
    hrp = np.where(header.values[0] == 'Hearing Reset Percentage')[0][0] + 1
    df4 = df4.iloc[2:, hrp:-2]
    df4.index = df4.iloc[:, 0]
    df4.drop(df4.columns[0], axis=1, inplace=True)
    df4.columns = header.values[0][np.where(header.values[0] == 'Hearing Reset Percentage')[0][0] + 2:-2]

    df4 = df4.replace('-', np.nan)

    df4.apply(lambda x: (round(x, 3) * 100))

    # dispositions
    df5 = pd.read_excel(uploaded_file, sheet_name=2, skiprows=5, usecols=list(range(1, 17))).T

    header = df5.iloc[:2]
    df5.index = df5.iloc[:, 0]
    df5 = df5.iloc[2:, 1:-5]

    dis_col = header.values[1][1:-6]
    df5.columns = np.append(dis_col, header.values[0][-6])

    # sealings
    df6 = pd.read_excel(uploaded_file, sheet_name=2, usecols=list(range(1, 17))).T

    df6 = df6.iloc[2:, np.where(df6.iloc[0] == 'Sealings')[0][0]: ]
    df6.columns = ['Month', 'Sealings']
    df6 = df6.set_index('Month')
       
    # detention
    df7 = pd.read_excel(uploaded_file, sheet_name=3, skiprows=4, usecols=list(range(1, 18))).T

    header = df7.iloc[1:3]
    df7 = df7.iloc[3:, :-2]
    col = header.values[1][:-2]
    df7.columns = col

    # caseloads
    df8 = pd.read_excel(uploaded_file, sheet_name=4, skiprows=4, usecols=list(range(1, 17))).T

    header = df8.iloc[:2]
    df8.index = df8.iloc[:, 0]
    df8 = df8.iloc[2:, 2:20]

    df8.columns = header.values[1][2:20]
    df8.drop(df8.columns[[5]], axis=1, inplace=True)

    # supervision
    df9 = pd.read_excel(uploaded_file, sheet_name=4, skiprows=28, usecols=list(range(1, 17))).T

    header = df9.iloc[:2]
    df9.index = df9.iloc[:, 0]
    df9 = df9.iloc[2:, 1:-2]

    df9.columns = header.values[0][1:-2]

    # internal placement
    df10 = pd.read_excel(uploaded_file, sheet_name=5, skiprows=4, usecols=list(range(1, 18))).T

    header = df10.iloc[:3]
    df10 = df10.iloc[3:, 1:-2]
    df10 = df10.dropna(axis=1, how='all')

    h1 = [x for x in header.values[1] if str(x) != 'nan']
    col_list = []

    for i in h1:
        for j in header.values[2][1:10]:
            ct = (i, j)
            c = ': '.join(ct)
            col_list.append(c)

    col_list.remove("Letot Intake: Successful")
    col_list.remove("Letot Intake: Unsuccessful")
    col_list.remove("Letot Intake: Administrative")
    col_list.remove("Letot Intake: Completion %")
    df10.columns = col_list

    letot_in_ph = np.where(df10.columns == df10.filter(like='Letot Intake: Total Exits').columns[0])[0][0]

    df10.insert(int(letot_in_ph + 1), "Dummy 1", 9999)
    df10.insert(int(letot_in_ph + 2), "Dummy 2", 9999)
    df10.insert(int(letot_in_ph + 3), "Dummy 3", 9999)
    df10.insert(int(letot_in_ph + 4), "Dummy 4", 9999)

    # internal placement
    df11 = pd.read_excel(uploaded_file, sheet_name=7, skiprows=3, usecols=list(range(1, 18))).T

    header = df11.iloc[:3]
    df11 = df11.iloc[3:, 1:-2]
    df11 = df11.dropna(axis=1, how='all')

    h1 = []
    h1.append([x for x in header.values[1] if str(x) != 'nan'][0])
    col_list = []

    for i in h1:
        for j in [x for x in header.values[2][:-1] if str(x) != 'nan'][:9]:
            ct = (i, j)
            c = ': '.join(ct)
            col_list.append(c)

    h2 = [x for x in header.values[1] if str(x) != 'nan'][1:]

    for i in h2:
        for j in [x for x in header.values[2][:-1] if str(x) != 'nan'][9:12]:
            ct = (i, j)
            c = ': '.join(ct)
            col_list.append(c)

    df11.columns = col_list

    # psych - Psychological Services Referrals
    df12 = pd.read_excel(uploaded_file, sheet_name=9, skiprows=6, usecols=list(range(1, 16))).T

    header = df12.iloc[0]
    df12 = df12.iloc[1:, : np.where(header.values == 'Total')[0][0]+1]
    df12.columns = header.values[:np.where(header.values == 'Total')[0][0]+1]

    # Behavioral Health
    df13 = pd.read_excel(uploaded_file, sheet_name=9).T

    df13.columns = df13.iloc[1]
    df13 = df13.iloc[:, :-1]
    df13 = df13.iloc[2:, np.where(df13.iloc[1] == 'Behavioral Health Services Referrals')[0][0]+1: np.where(df13.iloc[1] == 'Total')[0][1]+1]
    df13 = df13.set_index('Referred For')
    df13 = df13.loc[:'FY21 YTD Total', :]

    # Clinical Service Referral Outcomes
    df14 = pd.read_excel(uploaded_file, sheet_name=9).T

    df14.columns = df14.iloc[1]
    df14 = df14.iloc[:, :-1]
    df14 = df14.iloc[2:, np.where(df14.iloc[1] == 'Clinical Service Referral Outcomes')[0][0]+1: np.where(df14.iloc[1] == 'Behavioral Health Services Referrals Completed')[0][0]+1]
    df14 = df14.set_index('Referral Type')
    df14 = df14.loc[:'FY21 YTD Total', :]
    
    # education
    df15 = pd.read_excel(uploaded_file, sheet_name=10, skiprows=4, usecols=list(range(2, 18))).T

    header = df15.iloc[1]
    df15 = df15.iloc[2:, 1:-2]
    df15.columns = header.values[1:-2]

    # all refs (types)
    t_for_refs_ct = df.iloc[current_month_fy, 2]
    t_for_refs_prev = df.iloc[prev_month_fy, 2]
    t_for_refs_pct_chg = math.trunc(round((t_for_refs_ct / t_for_refs_prev) - 1, 2) * 100)

    # formal refs (offense)
    fel_refs_all_ct = sum(df2.iloc[current_month_fy, :5].values)
    fel_refs_all_prev = sum(df2.iloc[prev_month_fy, :5].values)
    fel_refs_all_pct_change = math.trunc(round((fel_refs_all_ct / fel_refs_all_prev) - 1, 2) * 100)

    mis_refs_all_ct = sum(df2.iloc[current_month_fy, 5:10].values)
    mis_refs_all_prev = sum(df2.iloc[prev_month_fy, 5:10].values)
    mis_refs_all_pct_change = math.trunc(round((mis_refs_all_ct / mis_refs_all_prev) - 1, 2) * 100)

    vop_refs_all_ct = (df2.iloc[current_month_fy, 10])
    vop_refs_all_prev = (df2.iloc[prev_month_fy, 10])
    vop_refs_all_pct_change = math.trunc(round((vop_refs_all_ct / vop_refs_all_prev) - 1, 2) * 100)

    cins_refs_all_ct = (df2.iloc[current_month_fy, 12])
    cins_refs_all_prev = (df2.iloc[prev_month_fy, 12])
    cins_refs_all_pct_change = math.trunc(round((cins_refs_all_ct / cins_refs_all_prev) - 1, 2) * 100)

    fel_t_22ytd = sum(df2.iloc[-2, :5].values)
    fel_t_21ytd = sum(df2.iloc[-1, :5].values)
    fel_t_22ytd_pct_chg = math.trunc(round((fel_t_22ytd / fel_t_21ytd) - 1, 2) * 100)

    fel_violent_ct = df2.iloc[-2, 0]
    fel_violent_prev = df2.iloc[-1, 0]
    fel_violent_22ytd_pct_chg = math.trunc(round((fel_violent_ct / fel_violent_prev) - 1, 2) * 100)

    fel_drugs_ct = df2.iloc[-2, 2]
    fel_drugs_prev = df2.iloc[-1, 2]
    fel_drugs_22ytd_pct_chg = math.trunc(round((fel_drugs_ct / fel_drugs_prev) - 1, 2) * 100)

    fel_weapons_ct = df2.iloc[-2, 3]
    fel_weapons_prev = df2.iloc[-1, 3]
    fel_weapons_22ytd_pct_chg = math.trunc(round((fel_weapons_ct / fel_weapons_prev) - 1, 2) * 100)

    mis_t_22ytd = sum(df2.iloc[-2, 5:10].values)
    mis_t_21ytd = sum(df2.iloc[-1, 5:10].values)
    mis_t_22ytd_pct_chg = math.trunc(round((mis_t_22ytd / mis_t_21ytd) - 1, 2) * 100)

    mis_violent_ct = df2.iloc[-2, 5]
    mis_violent_prev = df2.iloc[-1, 5]
    mis_violent_22ytd_pct_chg = math.trunc(round((mis_violent_ct / mis_violent_prev) - 1, 2) * 100)

    mis_vop_ct = df2.iloc[-2, 10]
    mis_vop_prev = df2.iloc[-1, 10]
    mis_vop_22ytd_pct_chg = math.trunc(round((mis_vop_ct / mis_vop_prev) - 1, 2) * 100)

    status_ct = df2.iloc[-2, 11]
    status_prev = df2.iloc[-1, 11]
    status_22ytd_pct_chg = math.trunc(round((status_ct / status_prev) - 1, 2) * 100)

    cins_ct = df2.iloc[-2, 12]
    cins_prev = df2.iloc[-1, 12]
    cins_22ytd_pct_chg = math.trunc(round((cins_ct / cins_prev) - 1, 2) * 100)

    # court hearings
    t_court_hearings_ct = df3.iloc[-2, df3.columns.get_loc("Total Held Detention Hearings")]
    t_court_hearings_prev= df3.iloc[-1, df3.columns.get_loc("Total Held Detention Hearings")]
    t_court_hearings_22ytd_pct_chg = math.trunc(round((cins_ct / cins_prev) - 1, 2) * 100)

    court_hear_reset_fy22 = math.trunc(round(df4.iloc[-2, -1], 2) * 100)
    court_hear_reset_fy21 = math.trunc(round(df4.iloc[-1, -1], 2) * 100)

    # all def pros
    def_pros_ct = df5.iloc[current_month_fy, 2]
    def_pros_ct2 = df5.iloc[current_month_fy, 6]
    def_pros_ct3 = df5.iloc[current_month_fy, 12]

    def_pros_prev = df5.iloc[prev_month_fy, 2]
    def_pros_prev2 = df5.iloc[prev_month_fy, 6]
    def_pros_prev3 = df5.iloc[prev_month_fy, 12]

    def_pros_pct_chg_mtm = math.trunc(round(((def_pros_ct + def_pros_ct2 + def_pros_ct3) / \
                                             (def_pros_prev + def_pros_prev2 + def_pros_prev3) - 1), 2) * 100)

    # Adjudicated to Probation
    adj_prob_ct = df5.iloc[current_month_fy, 13]
    adj_prob_prev = df5.iloc[prev_month_fy, 13]
    adj_prob_pct_chg_mtm = math.trunc(round(adj_prob_ct / adj_prob_prev - 1, 2) * 100)

    adj_prob_fy22_ytd = df5.iloc[-2, 13]
    adj_prob_fy21_ytd = df5.iloc[-1, 13]
    adj_prob_fy22_ytd_pct_chg = math.trunc(round(adj_prob_fy22_ytd / adj_prob_fy21_ytd - 1, 2) * 100)

    def_pros_ytd22 = df5.iloc[-2, 2]
    def_pros_ytd22_2 = df5.iloc[-2, 6]
    def_pros_ytd22_3 = df5.iloc[-2, 12]

    def_pros_ytd21 = df5.iloc[-1, 2]
    def_pros_ytd21_2 = df5.iloc[-1, 6]
    def_pros_ytd21_3 = df5.iloc[-1, 12]

    def_pros_pct_chg_ytd22 = math.trunc(round(((def_pros_ytd22 + def_pros_ytd22_2 + def_pros_ytd22_3) / \
                                               (def_pros_ytd21 + def_pros_ytd21_2 + def_pros_ytd21_3) - 1), 2) * 100)

    cert_adlt_fy22ytd = df5.iloc[-2, 18]
    cert_adlt_fy21ytd = df5.iloc[-1, 18]

    # sealings
    seals_ct = df6.iloc[current_month_fy, 0]
    seals_fy22ytd = df6.iloc[-2, 0]

    # detentions
    det_t_admin_ct = df7.iloc[current_month_fy, -5]
    det_t_admin_prev = df7.iloc[prev_month_fy, -5]
    det_t_admin_pct_chg_mtm = math.trunc(round((det_t_admin_ct / det_t_admin_prev) - 1, 2) * 100)

    det_t_exits_ct = df7.iloc[current_month_fy, -4]
    det_t_exits_prev = df7.iloc[prev_month_fy, -4]
    det_t_exits_pct_chg_mtm = math.trunc(round((det_t_exits_ct / det_t_exits_prev) - 1, 2) * 100)

    det_t_alos_ct = round(df7.iloc[current_month_fy, -2], 2)
    det_t_alos_prev = round(df7.iloc[prev_month_fy, -2], 2)

    det_t_adp_ct = round(df7.iloc[current_month_fy, -3], 0)
    det_t_adp_prev = round(df7.iloc[prev_month_fy, -3], 0)
    det_t_adp_pct_chg_mtm = math.trunc(round((det_t_adp_ct / det_t_adp_prev) - 1, 2) * 100)

    st.title('***Referrals***')
    st.write('\n')

    if t_for_refs_pct_chg > 0:
        st.write(
            'The Dallas County Juvenile Department (DCJD) received {} formalized referrals in {}, a {}% increase from the {} in {}.'.format(
                t_for_refs_ct, fy22[current_month_fy], t_for_refs_pct_chg, t_for_refs_prev, fy22[prev_month_fy]))
    else:
        st.write(
            'The Dallas County Juvenile Department (DCJD) received {} formalized referrals in {}, a {}% decrease from the {} in {}.'.format(
                t_for_refs_ct, fy22[current_month_fy], t_for_refs_pct_chg, t_for_refs_prev, fy22[prev_month_fy]))

    st.write(' ')
    st.write('Compared to the previous month, ')
    if fel_refs_all_pct_change > 0:
        st.write('• Felony referrals increased by {}% ({} vs. {})'.format(fel_refs_all_pct_change, fel_refs_all_ct, fel_refs_all_prev))
    else:
        st.write('• Felony referrals decreased by {}% ({} vs. {})'.format(fel_refs_all_pct_change, fel_refs_all_ct, fel_refs_all_prev))

    if mis_refs_all_pct_change > 0:
        st.write('• Misdemeanor referrals increased by {}% ({} vs. {})'.format(mis_refs_all_pct_change, mis_refs_all_ct, mis_refs_all_prev))
    else:
        st.write('• Misdemeanor referrals decreased by {}% ({} vs. {})'.format(mis_refs_all_pct_change, mis_refs_all_ct, mis_refs_all_prev))

    if vop_refs_all_pct_change > 0:
        st.write('• VOPs referrals increased by {}% ({} vs. {})'.format(vop_refs_all_pct_change, vop_refs_all_ct, vop_refs_all_prev))
    else:
        st.write('• VOPs referrals decreased by {}% ({} vs. {})'.format(vop_refs_all_pct_change, vop_refs_all_ct, vop_refs_all_prev))

    if cins_refs_all_pct_change > 0:
        st.write('• CINS referrals increased by {}% ({} vs. {})'.format(cins_refs_all_pct_change, cins_refs_all_ct, cins_refs_all_prev))
    else:
        st.write('• CINS referrals decreased by {}% ({} vs. {})'.format(cins_refs_all_pct_change, cins_refs_all_ct, cins_refs_all_prev))

    st.write(' ')

    st.write('Compared to the same months in FY2021,')
    if fel_t_22ytd_pct_chg > 0:
        st.write('   DCJD received {}% more felony referrals in FY2022 year-to-date'.format(fel_t_22ytd_pct_chg))
    else:
        st.write('   DCJD received {}% less felony referrals in FY2022 year-to-date'.format(fel_t_22ytd_pct_chg))

    if fel_violent_22ytd_pct_chg > 0:
        st.write('   including a {}% increase in violent felony referrals,'.format(fel_violent_22ytd_pct_chg))
    else:
        st.write('   including a {}% decrease in violent felony referrals,'.format(fel_violent_22ytd_pct_chg))

    if fel_drugs_22ytd_pct_chg > 0:
        st.write('   a {}% increase in felony drug referrals'.format(fel_drugs_22ytd_pct_chg))
    else:
        st.write('   a {}% decrease in felony drug referrals'.format(fel_drugs_22ytd_pct_chg))

    if fel_weapons_22ytd_pct_chg > 0:
        st.write('   a {}% increase in felony weapons referrals'.format(fel_weapons_22ytd_pct_chg))
    else:
        st.write('   a {}% decrease in felony weapons referrals'.format(fel_weapons_22ytd_pct_chg))

    st.write(' ')

    st.write('Through the same {} months,'.format(current_month_fy + 1))
    if mis_t_22ytd_pct_chg > 0:
        st.write('   DCJD received {}% more misdemeanor referrals compared to FY2021,'.format(mis_t_22ytd_pct_chg))
    else:
        st.write('   DCJD received {}% less misdemeanor referrals compared to FY2021,'.format(mis_t_22ytd_pct_chg))

    if mis_violent_22ytd_pct_chg > 0:
        st.write('   including an {}% increase in violent misdemeanors,'.format(mis_violent_22ytd_pct_chg))
    else:
        st.write('   including an {}% decrease in violent misdemeanors,'.format(mis_violent_22ytd_pct_chg))

    if mis_vop_22ytd_pct_chg > 0:
        st.write('   while also receiving nearly a {}% increase in VOP referrals,'.format(mis_vop_22ytd_pct_chg))
    else:
        st.write('   while also receiving nearly {}% decrease in VOP referrals,'.format(mis_vop_22ytd_pct_chg))

    if status_22ytd_pct_chg > 0:
        st.write('   {}% more status offense referrals,'.format(status_22ytd_pct_chg))
    else:
        st.write('   {}% fewer status offense referrals,'.format(status_22ytd_pct_chg))

    if cins_22ytd_pct_chg > 0:
        st.write('   and a {}% more CINS other than status referrals in FY2022.'.format(cins_22ytd_pct_chg))
    else:
        st.write('   and a {}% more CINS other than status referrals in FY2022.'.format(cins_22ytd_pct_chg))

    # court hearing
    st.write('\n')
    st.title('***Court Hearings***')
    st.write('\n')

    st.write('Compared to the first {} months of FY2021,'.format(current_month_fy + 1))
    if t_court_hearings_22ytd_pct_chg > 0:
        st.write('the number of detention hearings held in FY2022 increased by {}%, including:'.format(
            t_court_hearings_22ytd_pct_chg))
    else:
        st.write('the number of detention hearings held in FY2022 decreased by {}%, including:'.format(
            t_court_hearings_22ytd_pct_chg))

    try:
        for i in range(6):
            if (df3.iloc[-2, i] / df3.iloc[-1, i]) - 1 > 0:
                st.write('• a {}% increase in {} hearings.'.format(
                    math.trunc(round((df3.iloc[-2, i] / df3.iloc[-1, i]) - 1, 2) * 100),
                    df3.iloc[:, :6].columns[i]))
            else:
                st.write('• a {}% decrease in {} hearings.'.format(
                    math.trunc(round((df3.iloc[-2, i] / df3.iloc[-1, i]) - 1, 2) * 100),
                    df3.iloc[:, :6].columns[i]))
    except:
        pass

    # resets
    st.write('\n')
    if court_hear_reset_fy22 > court_hear_reset_fy21:
        st.write(
            'Court hearing resets are higher than the previous fiscal year: {}% of court hearings being reset in FY2022 year-to-date, compared to {}% of court hearings during the first {} months of FY2021.'.format(
                court_hear_reset_fy22, court_hear_reset_fy21, current_month_fy + 1))
    else:
        st.write(
            'Court hearing resets are lower than the previous fiscal year: {}% of court hearings being reset in FY2022 year-to-date, compared to {}% of court hearings during the first {} months of FY2021.'.format(
                court_hear_reset_fy22, court_hear_reset_fy21, current_month_fy + 1))

    st.write('\n')
    st.title('***Dispositions, Sealings***')
    st.write('\n')

    if def_pros_pct_chg_mtm > 0:
        st.write('The number of youths disposed to Deferred Prosecution had a month-to-month increase of {}% in {}'.format(
            def_pros_pct_chg_mtm, fy22[current_month_fy]))
    else:
        st.write('The number of youths disposed to Deferred Prosecution had a month-to-month decrease of {}% in {}'.format(
            def_pros_pct_chg_mtm, fy22[current_month_fy]))

    if adj_prob_pct_chg_mtm > 0:
        st.write('The number of youths adjudicated to Probation had a month-to-month increase of {}% in {}'.format(
            adj_prob_pct_chg_mtm, fy22[current_month_fy]))
    else:
        st.write('The number of youths adjudicated to Probation had a month-to-month decrease of {}% in {}'.format(
            adj_prob_pct_chg_mtm, fy22[current_month_fy]))

    if adj_prob_fy22_ytd_pct_chg > 0:
        st.write('Adjudications to Probation increase by {}% YTD FY2022 vs. YTD FY2021'.format(adj_prob_fy22_ytd_pct_chg))
    else:
        st.write('Adjudications to Probation decrease by {}% YTD FY2022 vs. YTD FY2021'.format(adj_prob_fy22_ytd_pct_chg))

    if def_pros_pct_chg_ytd22 > 0:
        st.write('Deferred Prosecution dispositions increase by {}% YTD FY2022 vs. YTD FY2021'.format(
            def_pros_pct_chg_ytd22))
    else:
        st.write('Deferred Prosecution dispositions decrease by {}% YTD FY2022 vs. YTD FY2021'.format(
            def_pros_pct_chg_ytd22))

    if def_pros_pct_chg_ytd22 > 0:
        st.write(
            '{} juveniles were certified as an adult through FY2022 YTD compared to {} certifications in FY2021 YTD'.format(
                cert_adlt_fy22ytd, cert_adlt_fy21ytd))

    st.write('The Records Unit sealed {} records in {}; {} sealings in FY22 YTD '.format(seals_ct, fy22[current_month_fy],
                                                                                      seals_fy22ytd))

    st.write('\n')
    st.title('***Detention***')
    st.write('\n')

    st.write('month-to-month total'.upper())

    try:
        for i in range(15, 21):
            if (df7.iloc[current_month_fy, i] / df7.iloc[prev_month_fy, i]) - 1 > 0:
                st.write('The total {} in {} increased by {}% compared to {} ({} vs. {})'.format(df7.columns[i],
                                                                                              fy22[current_month_fy],
                                                                                              math.trunc(round((
                                                                                                                           df7.iloc[
                                                                                                                               current_month_fy, i] /
                                                                                                                           df7.iloc[
                                                                                                                               prev_month_fy, i]) - 1,
                                                                                                               2) * 100),
                                                                                              fy22[prev_month_fy],
                                                                                              math.trunc(round(df7.iloc[
                                                                                                                   current_month_fy, i],
                                                                                                               2)),
                                                                                              math.trunc(round(df7.iloc[
                                                                                                                   prev_month_fy, i],
                                                                                                               2))))
            else:
                st.write('The total {} in {} decreased by {}% compared to {} ({} vs. {})'.format(df7.columns[i],
                                                                                              fy22[current_month_fy],
                                                                                              math.trunc(round((
                                                                                                                           df7.iloc[
                                                                                                                               current_month_fy, i] /
                                                                                                                           df7.iloc[
                                                                                                                               prev_month_fy, i]) - 1,
                                                                                                               2) * 100),
                                                                                              fy22[prev_month_fy],
                                                                                              math.trunc(round(df7.iloc[
                                                                                                                   current_month_fy, i],
                                                                                                               2)),
                                                                                              math.trunc(round(df7.iloc[
                                                                                                                   prev_month_fy, i],
                                                                                                               2))))
    except:
        pass

    st.write('\n')
    st.write('MONTH-TO-MONTH MALE')
    try:
        for i in range(1, 7):
            if (df7.iloc[current_month_fy, i] / df7.iloc[prev_month_fy, i]) - 1 > 0:
                st.write('The male {} in {} increased by {}% compared to {} ({} vs. {})'.format(df7.columns[i],
                                                                                             fy22[current_month_fy],
                                                                                             math.trunc(round((df7.iloc[
                                                                                                                   current_month_fy, i] /
                                                                                                               df7.iloc[
                                                                                                                   prev_month_fy, i]) - 1,
                                                                                                              2) * 100),
                                                                                             fy22[prev_month_fy],
                                                                                             math.trunc(round(df7.iloc[
                                                                                                                  current_month_fy, i],
                                                                                                              2)),
                                                                                             math.trunc(round(df7.iloc[
                                                                                                                  prev_month_fy, i],
                                                                                                              2))))
            else:
                st.write('The male {} in {} decreased by {}% compared to {} ({} vs. {})'.format(df7.columns[i],
                                                                                             fy22[current_month_fy],
                                                                                             math.trunc(round((df7.iloc[
                                                                                                                   current_month_fy, i] /
                                                                                                               df7.iloc[
                                                                                                                   prev_month_fy, i]) - 1,
                                                                                                              2) * 100),
                                                                                             fy22[prev_month_fy],
                                                                                             math.trunc(round(df7.iloc[
                                                                                                                  current_month_fy, i],
                                                                                                              2)),
                                                                                             math.trunc(round(df7.iloc[
                                                                                                                  prev_month_fy, i],
                                                                                                              2))))
    except:
        pass

    st.write('\n')
    st.write('MONTH-TO-MONTH FEMALE')
    try:
        for i in range(8, 15):
            if (df7.iloc[current_month_fy, i] / df7.iloc[prev_month_fy, i]) - 1 > 0:
                st.write('The female {} in {} increased by {}% compared to {} ({} vs. {})'.format(df7.columns[i],
                                                                                               fy22[current_month_fy],
                                                                                               math.trunc(round((
                                                                                                                            df7.iloc[
                                                                                                                                current_month_fy, i] /
                                                                                                                            df7.iloc[
                                                                                                                                prev_month_fy, i]) - 1,
                                                                                                                2) * 100),
                                                                                               fy22[prev_month_fy],
                                                                                               math.trunc(round(
                                                                                                   df7.iloc[
                                                                                                       current_month_fy, i],
                                                                                                   2)),
                                                                                               math.trunc(round(
                                                                                                   df7.iloc[
                                                                                                       prev_month_fy, i],
                                                                                                   2))))
            else:
                st.write('The female {} in {} decreased by {}% compared to {} ({} vs. {})'.format(df7.columns[i],
                                                                                               fy22[current_month_fy],
                                                                                               math.trunc(round((
                                                                                                                            df7.iloc[
                                                                                                                                current_month_fy, i] /
                                                                                                                            df7.iloc[
                                                                                                                                prev_month_fy, i]) - 1,
                                                                                                                2) * 100),
                                                                                               fy22[prev_month_fy],
                                                                                               math.trunc(round(
                                                                                                   df7.iloc[
                                                                                                       current_month_fy, i],
                                                                                                   2)),
                                                                                               math.trunc(round(
                                                                                                   df7.iloc[
                                                                                                       prev_month_fy, i],
                                                                                                   2))))
    except:
        pass

    # Caseloads
    st.write('\n')
    st.title('***Caseloads MTM***')
    st.write('\n')
    
    caseload_dict = {}
    cl_name = []
    cl_perc = []

       
    try:
        for i in range(0, 18):
            if (df8.iloc[current_month_fy, i] / df8.iloc[prev_month_fy, i]) - 1 > 0:
                   st.write('The average daily officer caseloads for the {} unit increased by {}% in {}, compared to {} ({} vs. {})'.format(df8.columns[i],
                                                                                                 math.trunc(round((df8.iloc[current_month_fy, i]/df8.iloc[prev_month_fy, i]) - 1, 2) * 100),
                                                                                                 fy22[current_month_fy], 
                                                                                                 fy22[prev_month_fy],                                         
                                                                                                 (round(df8.iloc[current_month_fy, i], 1)), 
                                                                                                 (round(df8.iloc[prev_month_fy, i], 1))))
                   cl_name.append(df8.columns[i])
                   cl_perc.append((df8.iloc[current_month_fy, i]/df8.iloc[prev_month_fy, i]) - 1)
            else:
                st.write('The average daily officer caseloads for the {} unit decreased by {}%  in {}, compared to {} ({} vs. {})'.format(df8.columns[i],
                                                                                          math.trunc(round((df8.iloc[current_month_fy, i]/df8.iloc[prev_month_fy, i]) - 1, 2) * 100),
                                                                                          fy22[current_month_fy], 
                                                                                          fy22[prev_month_fy],                                         
                                                                                          (round(df8.iloc[current_month_fy, i], 1)), 
                                                                                          (round(df8.iloc[prev_month_fy, i], 1))))
                cl_name.append(df8.columns[i])
                cl_perc.append((df8.iloc[current_month_fy, i]/df8.iloc[prev_month_fy, i]) - 1)

    except:
        pass

    caseload_dict ['Caseload Name'] = cl_name
    caseload_dict ['Caseload Perc. Change (MTM)'] = cl_perc
       
    # MTM
    cls = pd.DataFrame(caseload_dict).sort_values(by='Caseload Perc. Change (MTM)', ascending=False)
    st.subheader('Caseloads MTM Percent Change - Increases')
    st.write(cls[cls['Caseload Perc. Change (MTM)'] > 0].reset_index(drop=True).style.format({'Caseload Perc. Change (MTM)': '{:,.2%}'.format}))

    st.subheader('Caseloads MTM Percent Change -  Decreases')
    st.write(cls[cls['Caseload Perc. Change (MTM)'] < 0].sort_values(by='Caseload Perc. Change (MTM)').reset_index(drop=True).style.format({'Caseload Perc. Change (MTM)': '{:,.2%}'.format}))

       
    st.write('\n')
    st.title('***Caseloads YTD***')
    st.write('\n')

    caseload_dict2 = {}
    cl_name2 = []
    cl_perc2 = []

       
    try:
       for i in range(0, 18):
            if (df8.iloc[-2, i] / df8.iloc[-1, i]) - 1 > 0:
                st.write('The daily officer caseloads for the {} unit increased by {}% through {} FY2022 YTD, compared to FY2021 YTD ({} vs. {})'.format(df8.columns[i],
                                                                                          math.trunc(round((df8.iloc[-2, i]/df8.iloc[-1, i]) - 1, 2) * 100),
                                                                                          fy22[current_month_fy], 
                                                                                          (round(df8.iloc[-2, i], 1)), 
                                                                                          (round(df8.iloc[-1, i], 1))))
                cl_name2.append(df8.columns[i])
                cl_perc2.append((df8.iloc[-2, i]/df8.iloc[-1, i]) - 1)
            else:
                st.write('The average daily officer caseloads for the {} unit decreased by {}% through {} FY2022 YTD, compared to FY2021 YTD ({} vs. {})'.format(df8.columns[i],
                                                                                          math.trunc(round((df8.iloc[-2, i]/df8.iloc[-1, i]) - 1, 2) * 100),
                                                                                          fy22[current_month_fy], 
                                                                                          (round(df8.iloc[-2, i], 1)), 
                                                                                          (round(df8.iloc[-1, i], 1))))
                cl_name2.append(df8.columns[i])
                cl_perc2.append((df8.iloc[-2, i]/df8.iloc[-1, i]) - 1)
    except:
        pass 
       
    caseload_dict2 ['Caseload Name'] = cl_name2
    caseload_dict2 ['Caseload Perc. Change (YTD)'] = cl_perc2  
       
    # YTD
    cls2 = pd.DataFrame(caseload_dict2).sort_values(by='Caseload Perc. Change (YTD)', ascending=False)
    st.subheader('Caseloads YTD Percent Change - Increases')
    st.write(cls2[cls2['Caseload Perc. Change (YTD)'] > 0].reset_index(drop=True).style.format({'Caseload Perc. Change (YTD)': '{:,.2%}'.format}))

    st.subheader('Caseloads YTD Percent Change -  Decreases')
    st.write(cls2[cls2['Caseload Perc. Change (YTD)'] < 0].sort_values(by='Caseload Perc. Change (YTD)').reset_index(drop=True).style.format({'Caseload Perc. Change (YTD)': '{:,.2%}'.format}))
       

       
    st.write('\n')
    st.title('***Supervision MTM***')
    st.write('\n')

    try:
        for i in range(0, 6):
            if (df9.iloc[current_month_fy, i] / df9.iloc[prev_month_fy, i]) - 1 > 0:
                st.write(
                    'The average daily number of youths on {} Supervision in {} increased by {}% compared to {}, ({} vs. {})'.format(
                        df9.columns[i],
                        fy22[current_month_fy],
                        math.trunc(round((df9.iloc[current_month_fy, i] / df9.iloc[prev_month_fy, i]) - 1, 2) * 100),
                        fy22[prev_month_fy],
                        math.trunc(round(df9.iloc[current_month_fy, i], 2)),
                        math.trunc(round(df9.iloc[prev_month_fy, i], 2))))
            else:
                st.write(
                    'The average daily number of youths on {} Supervision in {} decreased by {}% compared to {}, ({} vs. {})'.format(
                        df9.columns[i],
                        fy22[current_month_fy],
                        math.trunc(round((df9.iloc[current_month_fy, i] / df9.iloc[prev_month_fy, i]) - 1, 2) * 100),
                        fy22[prev_month_fy],
                        math.trunc(round(df9.iloc[current_month_fy, i], 2)),
                        math.trunc(round(df9.iloc[prev_month_fy, i], 2))))
    except:
        pass

    st.write('\n')
    st.title('***Supervision YTD***')
    st.write('\n')

    try:
        for i in range(0, 6):
            if (df9.iloc[-2, i] / df9.iloc[-1, i]) - 1 > 0:
                st.write(
                    'The average daily number of youths on {} Supervision increased by {}% through {} FY2022 YTD, compared to FY2021 YTD ({} vs. {})'.format(
                        df9.columns[i],
                        math.trunc(round((df9.iloc[-2, i] / df9.iloc[-1, i]) - 1, 2) * 100),
                        fy22[current_month_fy],
                        math.trunc(round(df9.iloc[-2, i], 2)),
                        math.trunc(round(df9.iloc[-1, i], 2))))
            else:
                st.write(
                    'The average daily number of youths on {} Supervision decreased by {}% through {} FY2022 YTD, compared to FY2021 YTD ({} vs. {})'.format(
                        df9.columns[i],
                        math.trunc(round((df9.iloc[-2, i] / df9.iloc[-1, i]) - 1, 2) * 100),
                        fy22[current_month_fy],
                        math.trunc(round(df9.iloc[-2, i], 2)),
                        math.trunc(round(df9.iloc[-1, i], 2))))
    except:
        pass

    st.write('\n')
    st.title('***Internal Placement ADP MTM***')
    st.write('\n')

    int_pl_dict = {}
    pl_name = []
    pl_perc = []

    for i in range(7, 107, 9):
        try:
            if (df10.iloc[current_month_fy, i] / df10.iloc[prev_month_fy, i]) - 1 > 0:
                st.write('The ADP for {} increased by {}% in {}, compared to {} ({} vs. {})'.format(df10.columns[i],
                                                                                          math.trunc(round((df10.iloc[current_month_fy, i]/df10.iloc[prev_month_fy, i]) - 1, 2) * 100),
                                                                                          fy22[current_month_fy],
                                                                                          fy22[prev_month_fy],
                                                                                          (round(df10.iloc[current_month_fy, i], 1)), 
                                                                                          (round(df10.iloc[prev_month_fy, i], 1))))
                pl_name.append(df10.columns[i])
                pl_perc.append((df10.iloc[current_month_fy, i]/df10.iloc[prev_month_fy, i]) - 1)
            
            else:
                st.write('The ADP for {} decreased by {}% in {}, compared to {} ({} vs. {})'.format(df10.columns[i],
                                                                                          math.trunc(round((df10.iloc[current_month_fy, i]/df10.iloc[prev_month_fy, i]) - 1, 2) * 100),
                                                                                          fy22[current_month_fy],
                                                                                          fy22[prev_month_fy],
                                                                                          (round(df10.iloc[current_month_fy, i], 1)), 
                                                                                          (round(df10.iloc[prev_month_fy, i], 1))))
                pl_name.append(df10.columns[i])
                pl_perc.append((df10.iloc[current_month_fy, i]/df10.iloc[prev_month_fy, i]) - 1)
            
        except:
            pass
       
    int_pl_dict ['Placement'] = pl_name
    int_pl_dict ['Placement Perc. Change (MTM)'] = pl_perc     
    # MTM
    int_pl = pd.DataFrame(int_pl_dict).sort_values(by='Placement Perc. Change (MTM)', ascending=False)
    st.subheader('Internal Placement ADP MTM - Increases')
    st.write(int_pl[int_pl['Placement Perc. Change (MTM)'] > 0].reset_index(drop=True).style.format({'Placement Perc. Change (MTM)': '{:,.2%}'.format}))
    st.subheader('Internal Placement ADP MTM - Decreases')
    st.write(int_pl[int_pl['Placement Perc. Change (MTM)'] < 0].sort_values(by='Placement Perc. Change (MTM)').reset_index(drop=True).style.format({'Placement Perc. Change (MTM)': '{:,.2%}'.format}))
       
       
       
    st.write('\n')
    st.title('***Internal Placement ADP YTD***')
    st.write('\n')

    int_pl_dict2 = {}
    pl_name2 = []
    pl_perc2 = []

    for i in range(7, 107, 9):
        try:
            if (df10.iloc[-2, i] / df10.iloc[-1, i]) - 1 > 0:
                st.write('The ADP for {} increased by {}% in {} FY2022 YTD, compared to FY2021 YTD ({} vs. {})'.format(df10.columns[i],
                                                                                          math.trunc(round((df10.iloc[-2, i]/df10.iloc[-1, i]) - 1, 2) * 100),
                                                                                          fy22[current_month_fy],
                                                                                          (round(df10.iloc[-2, i], 1)), 
                                                                                          (round(df10.iloc[-1, i], 1))))
                pl_name2.append(df10.columns[i])
                pl_perc2.append((df10.iloc[-2, i]/df10.iloc[-1, i]) - 1)
            
            else:
                st.write('The ADP for {} decreased by {}% in {} FY2022 YTD, compared to FY2021 YTD ({} vs. {})'.format(df10.columns[i],
                                                                                          math.trunc(round((df10.iloc[-2, i]/df10.iloc[-1, i]) - 1, 2) * 100),
                                                                                          fy22[current_month_fy],
                                                                                          (round(df10.iloc[-2, i], 1)), 
                                                                                          (round(df10.iloc[-1, i], 1))))
                pl_name2.append(df10.columns[i])
                pl_perc2.append((df10.iloc[-2, i]/df10.iloc[-1, i]) - 1)
            
        except:
            pass

    int_pl_dict2 ['Placement Name'] = pl_name2
    int_pl_dict2 ['Placement Perc. Change (YTD)'] = pl_perc2

    # YTD
    int_pl2 = pd.DataFrame(int_pl_dict2).sort_values(by='Placement Perc. Change (YTD)', ascending=False)
    st.subheader('Internal Placement ADP YTD - Increases')
    st.write(int_pl2[int_pl2['Placement Perc. Change (YTD)'] > 0].reset_index(drop=True).style.format({'Placement Perc. Change (YTD)': '{:,.2%}'.format}))
    st.subheader('Internal Placement ADP YTD - Decreases')
    st.write(int_pl2[int_pl2['Placement Perc. Change (YTD)'] < 0].sort_values(by='Placement Perc. Change (YTD)').reset_index(drop=True).style.format({'Placement Perc. Change (YTD)': '{:,.2%}'.format}))


    st.write('\n')
    st.title('***Contract Placement***')
    st.write('\n')

    st.write('({}) youth were served at contract placement facilities in {}.'.format(df11.iloc[current_month_fy, 0],
                                                                                  fy22[current_month_fy]))
    st.write('There were ({}) admissions during {}.'.format(df11.iloc[current_month_fy, 1], fy22[current_month_fy]))
    st.write('There were ({}) exits during {}.'.format(df11.iloc[current_month_fy, 2], fy22[current_month_fy]))

    st.write('\n')
    st.write('***Psych/Clinical Services***')
    st.write('\n')

    if (df12.iloc[current_month_fy, -1] / df12.iloc[prev_month_fy, -1]) - 1 > 0:
        st.write(
            '({}) Psychological Services Referrals were made in {}, a {}% increase compared to  {} ({} vs. {})'.format(
                df12.iloc[current_month_fy, -1],
                fy22[current_month_fy],
                math.trunc(round((df12.iloc[current_month_fy, -1] / df12.iloc[prev_month_fy, -1]) - 1, 2) * 100),
                fy22[prev_month_fy],
                math.trunc(round(df12.iloc[current_month_fy, -1])),
                math.trunc(round(df12.iloc[prev_month_fy, -1]))))
    else:
        st.write('({}) Psychological Services Referrals were made in {}, a {}% decrease compared to {} ({} vs. {})'.format(
            df12.iloc[current_month_fy, -1],
            fy22[current_month_fy],
            math.trunc(round((df12.iloc[current_month_fy, -1] / df12.iloc[prev_month_fy, -1]) - 1, 2) * 100),
            fy22[prev_month_fy],
            math.trunc(round(df12.iloc[current_month_fy, -1])),
            math.trunc(round(df12.iloc[prev_month_fy, -1]))))

    if (df12.iloc[-2, -1] / df12.iloc[-1, -1]) - 1 > 0:
        st.write(
            'The number of Psychological Service Referrals made through the first {} months of FY2022 are up {}% compared to the same months in FY2021.'.format(
                current_month_fy + 1,
                math.trunc(round((df12.iloc[-2, -1] / df12.iloc[-1, -1]) - 1, 2) * 100)))
    else:
        st.write(
            'The number of Psychological Service Referrals made through the first {} months of FY2022 are down {}% compared to the same months in FY2021.'.format(
                current_month_fy + 1,
                math.trunc(round((df12.iloc[-2, -1] / df12.iloc[-1, -1]) - 1, 2) * 100)))

    st.write('\n')
    st.write('***Psych/Clinical Services YTD***')

    for i in range(0, df12.shape[1]):
        try:
            if (df12.iloc[-2, i] / df12.iloc[-1, i]) - 1 > 0:
                st.write(
                    'There was a {}% increase for {} referrals during the first {} months of FY2022 YTD, compared to the same months in FY2021. ({} vs. {})'.format(
                        math.trunc(round((df12.iloc[-2, i] / df12.iloc[-1, i]) - 1, 2) * 100),
                        df12.columns[i],
                        current_month_fy + 1,
                        math.trunc(round(df12.iloc[-2, i], 2)),
                        math.trunc(round(df12.iloc[-1, i], 2))))
            else:
                st.write(
                    'There was a {}% decrease for {} referrals during the first {} months of FY2022 YTD, compared to the same months in FY2021. ({} vs. {})'.format(
                        math.trunc(round((df12.iloc[-2, i] / df12.iloc[-1, i]) - 1, 2) * 100),
                        df12.columns[i],
                        current_month_fy + 1,
                        math.trunc(round(df12.iloc[-2, i], 2)),
                        math.trunc(round(df12.iloc[-1, i], 2))))
        except ZeroDivisionError:
            pass

    st.write('\n')
    st.write('***Psych/Behavioral Health Services Referrals MTM***')

    for i in range(0, df13.shape[1]):
        try:

            if (df13.iloc[current_month_fy, i] / df13.iloc[current_month_fy, i]) - 1 > 0:
                st.write(
                    'Behavioral Health Services: {} Referrals made during {} were up {}% compared to {} ({} vs. {}).'.format(
                        df13.columns[i],
                        fy22[current_month_fy],
                        math.trunc(round((df13.iloc[current_month_fy, i] / df13.iloc[prev_month_fy, i]) - 1, 2) * 100),
                        fy22[prev_month_fy],
                        math.trunc(round(df13.iloc[current_month_fy, i], 2)),
                        math.trunc(round(df13.iloc[prev_month_fy, i], 2))))
            else:
                st.write(
                    'Behavioral Health Services: {} Referrals made during {} were down {}% compared to {} ({} vs. {}).'.format(
                        df13.columns[i],
                        fy22[current_month_fy],
                        math.trunc(round((df13.iloc[current_month_fy, i] / df13.iloc[prev_month_fy, i]) - 1, 2) * 100),
                        fy22[prev_month_fy],
                        math.trunc(round(df13.iloc[current_month_fy, i], 2)),
                        math.trunc(round(df13.iloc[prev_month_fy, i], 2))))
        except ZeroDivisionError:
            pass

    st.write('\n')
    st.write('***Psych/Behavioral Health Services Referrals YTD***')

    for i in range(0, df13.shape[1]):
        try:

            if (df13.iloc[-2, i] / df13.iloc[-1, i]) - 1 > 0:
                st.write(
                    'Behavioral Health Services: {} Referrals made through {} FY2022 YTD were up {}% compared to FY2021 YTD ({} vs. {}).'.format(
                        df13.columns[i],
                        fy22[current_month_fy],
                        math.trunc(round((df13.iloc[-2, i] / df13.iloc[-1, i]) - 1, 2) * 100),
                        math.trunc(round(df13.iloc[-2, i], 2)),
                        math.trunc(round(df13.iloc[-1, i], 2))))
            else:
                st.write(
                    'Behavioral Health Services: {} Referrals made through {} FY2022 YTD were down {}% compared to FY2021 YTD ({} vs. {}).'.format(
                        df13.columns[i],
                        fy22[current_month_fy],
                        math.trunc(round((df13.iloc[-2, i] / df13.iloc[-1, i]) - 1, 2) * 100),
                        math.trunc(round(df13.iloc[-2, i], 2)),
                        math.trunc(round(df13.iloc[-1, i], 2))))
        except ZeroDivisionError:
            pass

    st.write('\n')
    st.write('***Psych/Clinical Service Referral Outcomes YTD***')
    st.write(
        'Through the first {} months of FY2022, {}% of all Psychological Services Referrals had a completed outcome,'.format(
            current_month_fy + 1,
            math.trunc(round(df14.iloc[-2, 0], 2) * 100),
            ))
    st.write(
        'Through the first {} months of FY2021, {}% of all Psychological Services Referrals had a completed outcome,'.format(
            current_month_fy + 1,
            math.trunc(round(df14.iloc[-1, 0], 2) * 100),
            ))
    st.write(
        'Through the first {} months of FY2022, {}% of all Behavioral Health Services Referrals had a completed outcome,'.format(
            current_month_fy + 1,
            math.trunc(round(df14.iloc[-2, 1], 2) * 100),
            ))
    st.write(
        'Through the first {} months of FY2021, {}% of all Behavioral Health Services Referrals had a completed outcome,'.format(
            current_month_fy + 1,
            math.trunc(round(df14.iloc[-1, 1], 2) * 100),
            ))
    st.write('\n')
    st.write('***Education***')
    st.write('\n')

    st.write(
        'The Dallas County JJAEP had seventeen ({}) admissions in January 2022.'.format(df15.iloc[current_month_fy, 4]))
    st.write('\n')

    for i in range(0, 13):
        try:

            if (df15.iloc[-2, i] / df15.iloc[-1, i]) - 1 > 0:
                st.write(
                    'Dallas County JJAEP had ({}) {} through {}, a {}% increase from the number served during the same months in FY2021 ({} vs. {}).'.format(
                        df15.iloc[-2, i],
                        df15.columns[i],
                        fy22[current_month_fy],
                        math.trunc(round((df15.iloc[-2, i] / df15.iloc[-1, i]) - 1, 2) * 100),
                        math.trunc(round(df15.iloc[-2, i], 2)),
                        math.trunc(round(df15.iloc[-1, i], 2))))
            else:
                st.write(
                    'Dallas County JJAEP had ({}) {} through {}, a {}% decrease from the number served during the same months in FY2021 ({} vs. {}).'.format(
                        df15.iloc[-2, i],
                        df15.columns[i],
                        fy22[current_month_fy],
                        math.trunc(round((df15.iloc[-2, i] / df15.iloc[-1, i]) - 1, 2) * 100),
                        math.trunc(round(df15.iloc[-2, i], 2)),
                        math.trunc(round(df15.iloc[-1, i], 2))))
        except ZeroDivisionError:
            pass

    st.write('\n')
    st.write(
        'There were ({}) total exits from JJAEP in {}, ({}) of whom discharged successfully, ({}) unsuccessfully, and ({}) other.'.format(
            df15.iloc[current_month_fy, 5],
            fy22[current_month_fy],
            df15.iloc[current_month_fy, 6],
            df15.iloc[current_month_fy, 7],
            df15.iloc[current_month_fy, 8]
            ))



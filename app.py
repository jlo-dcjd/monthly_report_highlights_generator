import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import math


# fy22 = [('OCT 2021'), ('NOV 2021'), ('DEC 2021'), ('JAN 2022'), ('FEB 2022'), ('MAR 2022'), ('APR 2022'), ('MAY 2022'),
#        ('JUN 2022'), ('JUL 2022'), ('AUG 2022'), ('September 2022')]


def month_index_cur():
    ''' Return iloc for current report month'''
    # Oct. - Nov.
    if datetime.now().month in (11, 12):
        return datetime.now().month - 11
    else:
        return datetime.now().month + 1


def month_index_prev():
    ''' Return iloc for previous report month'''
    # Oct. - Nov.
    if datetime.now().month == 12:
        return datetime.now().month - 12
    else:
        return datetime.now().month


def report_month_cur():
    ''' Return month year for current report month'''
    # Jan.
    if datetime.now().month == 1:
        return pd.to_datetime('{}-01-{}'.format(datetime.now().month + 11, datetime.now().year - 1)).strftime("%B %Y")
    else:
        return pd.to_datetime('{}-01-{}'.format(datetime.now().month - 1, datetime.now().year)).strftime("%B %Y")


def report_month_prev():
    ''' Return month year for previous report month'''
    # Jan.
    if datetime.now().month in (1, 2):
        return pd.to_datetime('{}-01-{}'.format(datetime.now().month + 10, datetime.now().year - 1)).strftime("%B %Y")
    else:
        return pd.to_datetime('{}-01-{}'.format(datetime.now().month - 2, datetime.now().year)).strftime("%B %Y")

st.title("Monthly Report Generator")

fy_current = st.text_input("Type current fiscal year:", 'FY2023')
fy_previous = st.text_input("Type previous fiscal year:", 'FY2022')


# current = fy22[datetime.now().month + 1]
# previous = fy22[datetime.now().month ]
#
# month = st.radio(
#      "Select month for the report:",
#      ('Latest Month ({})'.format(current), 'Previous Month ({})'.format(previous)))
#
#
# if month == 'Latest Month ({})'.format(current):
#     month_index_cur() = datetime.now().month + 1
#     month_index_prev() = datetime.now().month
#     st.write('You selected: report month ({}), previous month ({})'. format(report_month_cur(), report_month_prev()))
# else:
#     month_index_cur() = datetime.now().month
#     month_index_prev() = datetime.now().month - 1
#     st.write('You selected: report month ({}), previous month ({})'. format(report_month_cur(), report_month_prev()))

st.write('Current report month: ',report_month_cur())

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

    col_alt = ['Month', 'F Violent', 'F Property', 'F Drugs', 'F Weapons', 'F Other', 'M Violent',
       'M Property', 'M Drugs', 'M Weapons', 'M Other', 'O VOP', 'O Status',
       'O CINS Other than Status', 'Total Formalized Referrals']

    df2 = pd.read_excel(uploaded_file, sheet_name=0, usecols=list(range(1, 17))).T

    df2 = df2.iloc[2:, np.where(df2.iloc[0] == 'Formalized Referrals')[0][0]+1: np.where(df2.iloc[0] == 'Total Formalized Referrals')[0][1]+1]
    if df2.shape[1] == 15:
        df2.columns = col_alt
    if df2.shape[1] == 16:
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
    df3.columns = df3.columns.str.title()

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

    columns = [('Male', 'NA'), ('Male', 'Youth Served'), ('Male', 'Admissions'), ('Male', 'Total Exits'),
               ('Male', 'ADP'), ('Male', 'ALOS'), ('Male', 'Peak Population'),
               ('Female', 'NA'), ('Female', 'Youth Served'), ('Female', 'Admissions'), ('Female', 'Total Exits'),
               ('Female', 'ADP'), ('Female', 'ALOS'), ('Female', 'Peak Population'),
               ('Total', 'NA'), ('Total', 'Youth Served'), ('Total', 'Admissions'), ('Total', 'Total Exits'),
               ('Total', 'ADP'), ('Total', 'ALOS'), ('Total', 'Peak Population')
               ]

    df7.columns = pd.MultiIndex.from_tuples(columns)
    df7 = df7.drop([('Male', 'NA'), ('Female', 'NA'), ('Total', 'NA')], axis=1)

    # caseloads
    df8 = pd.read_excel(uploaded_file, sheet_name=4, skiprows=4, usecols=list(range(1, 17))).T

    header = df8.iloc[:2]
    df8.index = df8.iloc[:, 0]
    df8 = df8.iloc[2:, 2:20]

    df8.columns = header.values[1][2:20]
    df8.drop(df8.columns[[5]], axis=1, inplace=True)

    # supervision
    df9 = pd.read_excel(uploaded_file, sheet_name=4, usecols=list(range(1, 17))).T

    header = df9.iloc[0]
    df9 = df9.iloc[0:,
          np.where(header.values == 'Supervision Category')[0][0]: np.where(header.values == 'Total')[0][0] + 1]
    header2 = df9.iloc[0]

    df9.index = df9.iloc[:, 0]
    df9 = df9.iloc[2:, 1:]
    df9.columns = header2[1:]

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
    df12 = pd.read_excel(uploaded_file, sheet_name=10, skiprows=6, usecols=list(range(1, 16))).T

    header = df12.iloc[0]
    df12 = df12.iloc[1:, : np.where(header.values == 'Total')[0][0]+1]
    df12.columns = header.values[:np.where(header.values == 'Total')[0][0]+1]

    # Behavioral Health
    df13 = pd.read_excel(uploaded_file, sheet_name=10).T

    df13.columns = df13.iloc[1]
    df13 = df13.iloc[:, :-1]
    df13 = df13.iloc[2:, np.where(df13.iloc[1] == 'Behavioral Health Services Referrals')[0][0]+1: np.where(df13.iloc[1] == 'Total')[0][1]+1]
    df13 = df13.set_index('Referred For')
    try:
        df13 = df13.loc[:'FY21 YTD Total', :]
    except KeyError:
        df13 = df13.loc[:'FY21 Total', :]

    # Clinical Service Referral Outcomes
    df14 = pd.read_excel(uploaded_file, sheet_name=10).T

    df14.columns = df14.iloc[1]
    df14 = df14.iloc[:, :-1]
    df14 = df14.iloc[2:, np.where(df14.iloc[1] == 'Clinical Service Referral Outcomes')[0][0]+1: np.where(df14.iloc[1] == 'Behavioral Health Services Referrals Completed')[0][0]+1]
    df14 = df14.set_index('Referral Type')
    try:
        df13 = df13.loc[:'FY21 YTD Total', :]
    except KeyError:
        df13 = df13.loc[:'FY21 Total', :]

    # education
    df15 = pd.read_excel(uploaded_file, sheet_name=11, skiprows=4, usecols=list(range(2, 18))).T

    header = df15.iloc[1]
    df15 = df15.iloc[2:, 1:-2]
    df15.columns = header.values[1:-2]


    def round_pct_change(current, prev):
        return round(((current / prev) - 1) * 100)


    # all refs (types)
    t_for_refs_ct = df.iloc[month_index_cur(), 2]
    t_for_refs_prev = df.iloc[month_index_prev(), 2]
    t_for_refs_pct_chg = round_pct_change(t_for_refs_ct, t_for_refs_prev)

    # formal refs (offense)
    fel_refs_all_ct = sum(df2.iloc[month_index_cur(), :5].values)
    fel_refs_all_prev = sum(df2.iloc[month_index_prev(), :5].values)
    fel_refs_all_pct_change = round_pct_change(fel_refs_all_ct, fel_refs_all_prev)

    mis_refs_all_ct = sum(df2.iloc[month_index_cur(), 5:10].values)
    mis_refs_all_prev = sum(df2.iloc[month_index_prev(), 5:10].values)
    mis_refs_all_pct_change = round_pct_change(mis_refs_all_ct, mis_refs_all_prev)

    vop_refs_all_ct = (df2.iloc[month_index_cur(), 10])
    vop_refs_all_prev = (df2.iloc[month_index_prev(), 10])
    vop_refs_all_pct_change = round_pct_change(vop_refs_all_ct, vop_refs_all_prev)

    cins_refs_all_ct = (df2.iloc[month_index_cur(), 12])
    cins_refs_all_prev = (df2.iloc[month_index_prev(), 12])
    cins_refs_all_pct_change = round_pct_change(cins_refs_all_ct, cins_refs_all_prev)

    stat_refs_all_ct = (df2.iloc[month_index_cur(), 11])
    stat_refs_all_prev = (df2.iloc[month_index_prev(), 11])
    stat_refs_all_pct_change = round_pct_change(stat_refs_all_ct, stat_refs_all_prev)

    fel_t_22ytd = sum(df2.iloc[-2, :5].values)
    fel_t_21ytd = sum(df2.iloc[-1, :5].values)
    fel_t_22ytd_pct_chg = round_pct_change(fel_t_22ytd, fel_t_21ytd)

    fel_violent_ct = df2.iloc[-2, 0]
    fel_violent_prev = df2.iloc[-1, 0]
    fel_violent_22ytd_pct_chg = round_pct_change(fel_violent_ct, fel_violent_prev)

    fel_drugs_ct = df2.iloc[-2, 2]
    fel_drugs_prev = df2.iloc[-1, 2]
    fel_drugs_22ytd_pct_chg = round_pct_change(fel_drugs_ct, fel_drugs_prev)

    fel_weapons_ct = df2.iloc[-2, 3]
    fel_weapons_prev = df2.iloc[-1, 3]
    fel_weapons_22ytd_pct_chg = round_pct_change(fel_weapons_ct, fel_weapons_prev)

    mis_t_22ytd = sum(df2.iloc[-2, 5:10].values)
    mis_t_21ytd = sum(df2.iloc[-1, 5:10].values)
    mis_t_22ytd_pct_chg = round_pct_change(mis_t_22ytd, mis_t_21ytd)

    mis_violent_ct = df2.iloc[-2, 5]
    mis_violent_prev = df2.iloc[-1, 5]
    mis_violent_22ytd_pct_chg = round_pct_change(mis_violent_ct, mis_violent_prev)

    mis_vop_ct = df2.iloc[-2, 10]
    mis_vop_prev = df2.iloc[-1, 10]
    mis_vop_22ytd_pct_chg = round_pct_change(mis_vop_ct, mis_vop_prev)

    status_ct = df2.iloc[-2, 11]
    status_prev = df2.iloc[-1, 11]
    status_22ytd_pct_chg = round_pct_change(status_ct, status_prev)

    cins_ct = df2.iloc[-2, 12]
    cins_prev = df2.iloc[-1, 12]
    cins_22ytd_pct_chg = round_pct_change(cins_ct, cins_prev)

    # court hearings
    t_court_hearings_ct = df3.iloc[-2, df3.columns.get_loc("Total Held Detention Hearings")]
    t_court_hearings_prev= df3.iloc[-1, df3.columns.get_loc("Total Held Detention Hearings")]
    t_court_hearings_22ytd_pct_chg = round_pct_change(t_court_hearings_ct, t_court_hearings_prev)



    court_hear_reset_fy22 = math.trunc(round(df4.iloc[-2, -1], 2) * 100)
    court_hear_reset_fy21 = math.trunc(round(df4.iloc[-1, -1], 2) * 100)

    # Deferred Prosecution MTM
    def_pros_ct = df5.iloc[month_index_cur(), np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][0]]
    def_pros_ct2 = df5.iloc[month_index_cur(), np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][1]]
    def_pros_ct3 = df5.iloc[month_index_cur(), np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][2]]

    def_pros_prev = df5.iloc[month_index_prev(), np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][0]]
    def_pros_prev2 = df5.iloc[month_index_prev(), np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][1]]
    def_pros_prev3 = df5.iloc[month_index_prev(), np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][2]]

    def_pros_pct_chg_mtm = math.trunc(round(((def_pros_ct + def_pros_ct2 + def_pros_ct3) / \
                                             (def_pros_prev + def_pros_prev2 + def_pros_prev3) - 1), 2) * 100)

    # Adjudicated to Probation
    adj_prob_ct = df5.iloc[month_index_cur(), df5.columns.get_loc('Adjudicated to Probation')]
    adj_prob_prev = df5.iloc[month_index_prev(), df5.columns.get_loc('Adjudicated to Probation')]
    adj_prob_pct_chg_mtm = round_pct_change(adj_prob_ct, adj_prob_prev)

    adj_prob_fy22_ytd = df5.iloc[-2, df5.columns.get_loc('Adjudicated to Probation')]
    adj_prob_fy21_ytd = df5.iloc[-1, df5.columns.get_loc('Adjudicated to Probation')]
    adj_prob_fy22_ytd_pct_chg = round_pct_change(adj_prob_fy22_ytd, adj_prob_fy21_ytd)

    # Deferred Prosecution YTD
    def_pros_ytd22 = df5.iloc[-2, np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][0]]
    def_pros_ytd22_2 = df5.iloc[-2, np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][1]]
    def_pros_ytd22_3 = df5.iloc[-2, np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][2]]

    def_pros_ytd21 = df5.iloc[-1, np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][0]]
    def_pros_ytd21_2 = df5.iloc[-1, np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][1]]
    def_pros_ytd21_3 = df5.iloc[-1, np.where(df5.columns.get_loc('Deferred Prosecution') == True)[0][2]]

    def_pros_pct_chg_ytd22 = math.trunc(round(((def_pros_ytd22 + def_pros_ytd22_2 + def_pros_ytd22_3) / \
                                               (def_pros_ytd21 + def_pros_ytd21_2 + def_pros_ytd21_3) - 1), 2) * 100)

    cert_adlt_fy22ytd = df5.iloc[-2, df5.columns.get_loc("Certified as an Adult")]
    cert_adlt_fy21ytd = df5.iloc[-1, df5.columns.get_loc("Certified as an Adult")]

    # sealings
    seals_ct = df6.iloc[month_index_cur(), 0]
    seals_fy22ytd = df6.iloc[-2, 0]

    # detentions
    det_t_admin_ct = df7.iloc[month_index_cur(), -5]
    det_t_admin_prev = df7.iloc[month_index_prev(), -5]
    det_t_admin_pct_chg_mtm =  round_pct_change(det_t_admin_ct, det_t_admin_prev)

    det_t_exits_ct = df7.iloc[month_index_cur(), -4]
    det_t_exits_prev = df7.iloc[month_index_prev(), -4]
    det_t_exits_pct_chg_mtm = round_pct_change(det_t_exits_ct, det_t_exits_prev)

    det_t_alos_ct = round(df7.iloc[month_index_cur(), -2], 2)
    det_t_alos_prev = round(df7.iloc[month_index_prev(), -2], 2)

    det_t_adp_ct = round(df7.iloc[month_index_cur(), -3], 0)
    det_t_adp_prev = round(df7.iloc[month_index_prev(), -3], 0)
    det_t_adp_pct_chg_mtm = round_pct_change(det_t_adp_ct, det_t_adp_prev)



    st.markdown("---")
    st.title('***Referrals***')
    st.write('\n')

    if t_for_refs_pct_chg > 0:
        st.write(
            'The Dallas County Juvenile Department (DCJD) received {} formalized referrals in {}, a {}% increase from the {} in {}.'.format(
                t_for_refs_ct, report_month_cur(), t_for_refs_pct_chg, t_for_refs_prev, report_month_prev()))
    else:
        st.write(
            'The Dallas County Juvenile Department (DCJD) received {} formalized referrals in {}, a {}% decrease from the {} in {}.'.format(
                t_for_refs_ct, report_month_cur(), t_for_refs_pct_chg, t_for_refs_prev, report_month_prev()))

    st.write(' ')

    ref_list_mtm = []

    if fel_refs_all_pct_change > 0:
        ref_list_mtm.append('Compared to the previous month, felony referrals increased by {}%,'.format(fel_refs_all_pct_change))
    else:
        ref_list_mtm.append('Compared to the previous month, felony referrals decrease by {}%,'.format(fel_refs_all_pct_change))

    if mis_refs_all_pct_change > 0:
        ref_list_mtm.append('misdemeanor referrals increased by {}%,'.format(mis_refs_all_pct_change))
    else:
        ref_list_mtm.append('misdemeanor referrals decrease by {}%,'.format(mis_refs_all_pct_change))

    if vop_refs_all_pct_change > 0:
        ref_list_mtm.append('VOPs referrals increased by {}%,'.format(vop_refs_all_pct_change))
    else:
        ref_list_mtm.append('VOPs referrals decrease by {}%,'.format(vop_refs_all_pct_change))

    if cins_refs_all_pct_change > 0:
        ref_list_mtm.append('CINS referrals increased by {}%.'.format(cins_refs_all_pct_change))
    else:
        ref_list_mtm.append('CINS referrals decrease by {}%.'.format(cins_refs_all_pct_change))

    st.write(' '.join(ref_list_mtm))
    st.write(' ')

    ref_list_ytd = []

    st.write('Compared to the same months in {},'.format(fy_previous))

    if fel_t_22ytd_pct_chg > 0:
        ref_list_ytd.append(
            'DCJD received {}% more felony referrals in {} year-to-date,'.format(fel_t_22ytd_pct_chg, fy_current))
    else:
        ref_list_ytd.append(
            'DCJD received {}% less felony referrals in {} year-to-date,'.format(fel_t_22ytd_pct_chg, fy_current))

    if fel_violent_22ytd_pct_chg > 0:
        ref_list_ytd.append('including a {}% increase in violent felony referrals,'.format(fel_violent_22ytd_pct_chg))
    else:
        ref_list_ytd.append('including a {}% decrease in violent felony referrals,'.format(fel_violent_22ytd_pct_chg))

    if fel_drugs_22ytd_pct_chg > 0:
        ref_list_ytd.append('a {}% increase in felony drug referrals'.format(fel_drugs_22ytd_pct_chg))
    else:
        ref_list_ytd.append('a {}% decrease in felony drug referrals'.format(fel_drugs_22ytd_pct_chg))

    if fel_weapons_22ytd_pct_chg > 0:
        ref_list_ytd.append('a {}% increase in felony weapons referrals.'.format(fel_weapons_22ytd_pct_chg))
    else:
        ref_list_ytd.append('a {}% decrease in felony weapons referrals.'.format(fel_weapons_22ytd_pct_chg))

    st.write(' '.join(ref_list_ytd))
    st.write(' ')

    st.write('Through the same {} months,'.format(month_index_cur() + 1))

    ref_m_list_ytd = []

    if mis_t_22ytd_pct_chg > 0:
        ref_m_list_ytd.append(
            'DCJD received {}% more misdemeanor referrals compared to {},'.format(mis_t_22ytd_pct_chg, fy_previous))
    else:
        ref_m_list_ytd.append(
            'DCJD received {}% less misdemeanor referrals compared to {},'.format(mis_t_22ytd_pct_chg, fy_previous))

    if mis_violent_22ytd_pct_chg > 0:
        ref_m_list_ytd.append('including an {}% increase in violent misdemeanors,'.format(mis_violent_22ytd_pct_chg))
    else:
        ref_m_list_ytd.append('including an {}% decrease in violent misdemeanors,'.format(mis_violent_22ytd_pct_chg))

    if mis_vop_22ytd_pct_chg > 0:
        ref_m_list_ytd.append(
            'while also receiving nearly a {}% increase in VOP referrals,'.format(mis_vop_22ytd_pct_chg))
    else:
        ref_m_list_ytd.append(
            'while also receiving nearly {}% decrease in VOP referrals,'.format(mis_vop_22ytd_pct_chg))

    if status_22ytd_pct_chg > 0:
        ref_m_list_ytd.append('{}% more status offense referrals,'.format(status_22ytd_pct_chg))
    else:
        ref_m_list_ytd.append('{}% fewer status offense referrals,'.format(status_22ytd_pct_chg))

    if cins_22ytd_pct_chg > 0:
        ref_m_list_ytd.append('and a {}% more CINS other than status referrals in {}.'.format(cins_22ytd_pct_chg, fy_current))
    else:
        ref_m_list_ytd.append('and a {}% more CINS other than status referrals in {}.'.format(cins_22ytd_pct_chg, fy_current))

    st.write(' '.join(ref_m_list_ytd))



    st.markdown("---")
    # court hearing
    st.write('\n')
    st.title('***Court Hearings & Dispositions***')
    st.write('\n')

    det_hear_list = []

    if t_court_hearings_22ytd_pct_chg > 0:
        det_hear_list.append('Compared to the first {} months of {}, the number of detention hearings held in {} increased by {}%, including'.format(
            month_index_cur() + 1,
            fy_previous,
            fy_current,
            t_court_hearings_22ytd_pct_chg))
    else:
        det_hear_list.append('Compared to the first {} months of {}, the number of detention hearings held in {} decreased by {}%, including'.format(
            month_index_cur() + 1,
            fy_previous,
            fy_current,
            t_court_hearings_22ytd_pct_chg))

    for i in range(6):
        try:
            if (df3.iloc[-2, i] / df3.iloc[-1, i]) - 1 > 0:
                det_hear_list.append('a {}% increase in {} hearings,'.format(
                    math.trunc(round((df3.iloc[-2, i] / df3.iloc[-1, i]) - 1, 2) * 100),
                    df3.iloc[:, :6].columns[i]))
            else:
                det_hear_list.append('a {}% decrease in {} hearings,'.format(
                    math.trunc(round((df3.iloc[-2, i] / df3.iloc[-1, i]) - 1, 2) * 100),
                    df3.iloc[:, :6].columns[i]))
        except:
            pass


    non_det_hearings = (((df3.iloc[-2, -1] - df3.iloc[-2, df3.columns.get_loc('Total Held Detention Hearings')]) / (df3.iloc[-1, -1] - df3.iloc[-1, df3.columns.get_loc('Total Held Detention Hearings')]) - 1).round(2)*100).astype(int)

    if non_det_hearings > 0:
        det_hear_list.append('and non-detention hearings increased by {}%.'.format(
            non_det_hearings))
    else:
        det_hear_list.append('and non-detention hearings decreased by {}%.'.format(
            non_det_hearings))


    st.write(' '.join(det_hear_list))


    # resets
    st.write('\n')
    if court_hear_reset_fy22 > court_hear_reset_fy21:
        st.write(
            'Court hearing resets are higher than the previous fiscal year — {}% of court hearings being reset in {} year-to-date, compared to {}% of court hearings during the first {} months of {}.'.format(
                court_hear_reset_fy22, fy_current, court_hear_reset_fy21, month_index_cur() + 1, fy_previous))
    else:
        st.write(
            'Court hearing resets are lower than the previous fiscal year — {}% of court hearings being reset in {} year-to-date, compared to {}% of court hearings during the first {} months of {}.'.format(
                court_hear_reset_fy22, fy_current, court_hear_reset_fy21, month_index_cur() + 1, fy_previous))


    # Dispositions
    disp_list = []
    st.write('\n')

    if def_pros_pct_chg_mtm > 0:
        disp_list.append('The number of youths disposed to Deferred Prosecution had a month-to-month increase of {}% in {},'.format(
            def_pros_pct_chg_mtm, report_month_cur()))
    else:
        disp_list.append('The number of youths disposed to Deferred Prosecution had a month-to-month decrease of {}% in {},'.format(
            abs(def_pros_pct_chg_mtm), report_month_cur()))

    if adj_prob_pct_chg_mtm > 0:
        disp_list.append('adjudicated to Probation had a month-to-month increase of {}%.'.format(
            adj_prob_pct_chg_mtm, report_month_cur()))
    else:
        disp_list.append('adjudicated to Probation had a month-to-month decrease of {}%.'.format(
            abs(adj_prob_pct_chg_mtm), report_month_cur()))

    if adj_prob_fy22_ytd_pct_chg > 0:
        disp_list.append('Adjudications to Probation increased by {}% {} YTD compared to {} YTD,'.format(adj_prob_fy22_ytd_pct_chg, fy_current, fy_previous))
    else:
        disp_list.append('Adjudications to Probation decreased by {}% {} YTD compared to {} YTD,'.format(adj_prob_fy22_ytd_pct_chg, fy_current, fy_previous))

    if def_pros_pct_chg_ytd22 > 0:
        disp_list.append('and Deferred Prosecution dispositions increased by {}% {} YTD compared to {} YTD.'.format(def_pros_pct_chg_ytd22,
            fy_current, fy_previous))
    else:
        disp_list.append('and Deferred Prosecution dispositions decreased by {}% {} YTD compared to {} YTD.'.format(
            def_pros_pct_chg_ytd22, fy_current, fy_previous))

    if def_pros_pct_chg_ytd22 > 0:
        disp_list.append(
            'Finally, {} juveniles were certified as an adult through {} YTD compared to {} certifications in {} YTD.'.format(
                cert_adlt_fy22ytd, fy_current, cert_adlt_fy21ytd, fy_previous))

    st.write(' '.join(disp_list))



    st.markdown('---')
    st.write('\n')
    st.title('***Sealings***')
    st.write('\n')



    st.write('The Records Unit sealed {} records in {}, bringing the {} YTD total to {}.'.format(seals_ct, report_month_cur(), fy_current,
                                                                                      seals_fy22ytd))



    st.markdown("---")
    st.write('\n')
    st.title('***Detention***')

    # Detention Admissions
    det_admit_list = []

    if df7.iloc[month_index_cur(), 13] / df7.iloc[ month_index_prev(), 13] - 1 > 0:
        det_admit_list.append('DCJD had {} admissions to detention in {}, a {}% increase from {}.'.format(
            int(df7.iloc[month_index_cur(), 13]),
            report_month_cur(),
            round((df7.iloc[month_index_cur(), 13] / df7.iloc[ month_index_prev(), 13] - 1)*100),
            report_month_prev()))
    else:
        det_admit_list.append('DCJD had {} admissions to detention in {}, a {}% decrease from {}.'.format(
            int(df7.iloc[month_index_cur(), 13]),
            report_month_cur(),
            abs(round((df7.iloc[month_index_cur(), 13] / df7.iloc[month_index_prev(), 13] - 1) * 100)),
            report_month_prev()))


    det_admissions_ytd_pct_change = round((((df7.loc['FY22 Total', ('Total', 'Admissions')]) / (df7.loc['FY21 Total', ('Total', 'Admissions')]) - 1) * 100))

    if det_admissions_ytd_pct_change > 0:
        det_admit_list.append('The {} total detention admissions through the first {} months of {} are {}% higher than the total admissions during the same months of the previous fiscal year.'.format(
            int(df7.loc['FY22 Total', ('Total', 'Admissions')]),
            month_index_cur()+1,
            fy_current,
            det_admissions_ytd_pct_change))
    else:
        det_admit_list.append('The {} total detention admissions through the first {} months of {} are {}% lower than the total admissions during the same months of the previous fiscal year.'.format(
            int(df7.loc['FY22 Total', ('Total', 'Admissions')]),
            month_index_cur()+1,
            fy_current,
            det_admissions_ytd_pct_change))

    st.write(' '.join(det_admit_list))


    # Detention Exits
    detlist2 = []
    if round((df7.iloc[month_index_cur(), 14] / df7.iloc[ month_index_prev(), 14] - 1)*100) > 0:
        detlist2.append('The total number of exits from detention in {} increased by {}% compared to the previous month.'.format(
            report_month_cur(),
            round((df7.iloc[month_index_cur(), 14] / df7.iloc[month_index_prev(), 14] - 1) * 100)))
    else:
        detlist2.append('The total number of exits from detention in {} decreased by {}% compared to the previous month.'.format(
            report_month_cur(),
            round((df7.iloc[month_index_cur(), 14] / df7.iloc[month_index_prev(), 14] - 1) * 100)))


    if round((df7.iloc[month_index_cur(), 16] / df7.iloc[ month_index_prev(), 16] - 1)*100) > 0:
        detlist2.append('For youth who exited detention during the month, the Average Length of Stay was {} days, a {}% increase from {} ALOS of {} days.'.format(
                    round(df7.iloc[month_index_cur(), 16], 1),
                    round((df7.iloc[month_index_cur(), 16] / df7.iloc[ month_index_prev(), 16] - 1)*100),
                    report_month_prev().split()[0] + '\'s',
                    round(df7.iloc[month_index_prev(), 16], 1)
                    ))
    else:
        detlist2.append(
            'For youth who exited detention during the month, the Average Length of Stay was {} days, a {}% decrease from {} ALOS of {} days.'.format(
                round(df7.iloc[month_index_cur(), 16], 1),
                abs(round((df7.iloc[month_index_cur(), 16] / df7.iloc[month_index_prev(), 16] - 1) * 100)),
                report_month_prev().split()[0] + '\'s',
                round(df7.iloc[month_index_prev(), 16], 1)
            ))

    if round((df7.iloc[month_index_cur(), 4] / df7.iloc[ month_index_prev(), 4] - 1)*100) > 0:
        detlist2.append('The monthly ALOS for males released in {} increased by {}% ({} to {} days)'.format(
            report_month_prev().split()[0],
            abs(round((df7.iloc[month_index_cur(), 4] / df7.iloc[month_index_prev(), 4] - 1) * 100)),
            round(df7.iloc[month_index_prev(), 4]),
            round(df7.iloc[month_index_cur(), 4])
        ))
    else:
        detlist2.append('The monthly ALOS for males released in {} decreased by {}% ({} to {} days)'.format(
            report_month_prev().split()[0],
            abs(round((df7.iloc[month_index_cur(), 4] / df7.iloc[month_index_prev(), 4] - 1) * 100)),
            round(df7.iloc[month_index_prev(), 4]),
            round(df7.iloc[month_index_cur(), 4])
        ))

    if round((df7.iloc[month_index_cur(), 10] / df7.iloc[ month_index_prev(), 10] - 1)*100) > 0:
        detlist2.append(('and the ALOS for females increased by {}% ({} to {} days) compared to the previous month.'.format(
                        abs(round((df7.iloc[month_index_cur(), 10] / df7.iloc[ month_index_prev(), 10] - 1)*100)),
                        round(df7.iloc[month_index_prev(), 10]),
                        round(df7.iloc[month_index_cur(), 10])
                        )))
    else:
        detlist2.append(
            ('and the ALOS for females decreased by {}% ({} to {} days) compared to the previous month.'.format(
                abs(round((df7.iloc[month_index_cur(), 10] / df7.iloc[month_index_prev(), 10] - 1) * 100)),
                round(df7.iloc[month_index_prev(), 10]),
                round(df7.iloc[month_index_cur(), 10])
            )))

    st.write(' '.join(detlist2))

    # Detention ADP
    detlist3 = []

    if round((df7.iloc[month_index_cur(), 15] / df7.iloc[month_index_prev(), 15] - 1) * 100) > 0:
        detlist3.append('The Average Daily Population (ADP) in {} was {}, a {}% increase from {}'.format(
            report_month_cur(),
            round(df7.iloc[month_index_cur(), 15], 1),
            round((df7.iloc[month_index_cur(), 15] / df7.iloc[month_index_prev(), 15] - 1) * 100),
            report_month_prev()
        ))
    else:
        detlist3.append('The Average Daily Population (ADP) in {} was {}, a {}% decrease from {}'.format(
            report_month_cur(),
            round(df7.iloc[month_index_cur(), 15], 1),
            abs(round((df7.iloc[month_index_cur(), 15] / df7.iloc[month_index_prev(), 15] - 1) * 100)),
            report_month_prev()
        ))

    if round((df7.iloc[-2, 15] / df7.iloc[-1, 15] - 1)*100) > 0:
        detlist3.append(('The {} Detention ADP was {}% higher than that of the previous fiscal year, increasing from {} in {} to {}.'.format(
                fy_current,
                round((df7.iloc[-2, 15] / df7.iloc[-1, 15] - 1)*100),
                round(df7.iloc[-1, 15], 1),
                fy_previous,
                round(df7.iloc[-2, 15], 1)
            )))
    else:
        detlist3.append(('The {} Detention ADP was {}% lower than that of the previous fiscal year, decreasing from {} in {} to {}.'.format(
                fy_current,
                abs(round((df7.iloc[-2, 15] / df7.iloc[-1, 15] - 1)*100)),
                round(df7.iloc[-1, 15], 1),
                fy_previous,
                round(df7.iloc[-2, 15], 1)
            )))


    st.write(' '.join(detlist3))

    st.write('\n')

    # st.write('MONTH-TO-MONTH TOTAL')
    # for i in range(12, 17):
    #     try:
    #         if (df7.iloc[month_index_cur(), i] / df7.iloc[month_index_prev(), i]) - 1 > 0:
    #             st.write('The total {} in {} increased by {}% compared to {} ({} vs. {})'.format(df7.columns[i][1],
    #                                                                                           report_month_cur(),
    #                                                                                           round((df7.iloc[month_index_cur(), i] / df7.iloc[ month_index_prev(), i] - 1)*100),
    #                                                                                           report_month_prev(),
    #                                                                                           (round(df7.iloc[month_index_cur(), i], 2)),
    #                                                                                           (round(df7.iloc[month_index_prev(), i], 2))))
    #         else:
    #             st.write('The total {} in {} decreased by {}% compared to {} ({} vs. {})'.format(df7.columns[i][1],
    #                                                                                           report_month_cur(),
    #                                                                                           round((df7.iloc[month_index_cur(), i] / df7.iloc[ month_index_prev(), i] - 1)*100),
    #                                                                                           report_month_prev(),
    #                                                                                           (round(df7.iloc[month_index_cur(), i], 2)),
    #                                                                                           (round(df7.iloc[month_index_prev(), i], 2))))
    #     except:
    #         pass
    #
    # st.write('\n')
    # st.write('MONTH-TO-MONTH MALE')
    # for i in range(1, 5):
    #     try:
    #         if (df7.iloc[month_index_cur(), i] / df7.iloc[month_index_prev(), i]) - 1 > 0:
    #             st.write('The male {} in {} increased by {}% compared to {} ({} vs. {})'.format(df7.columns[i][1],
    #                                                                                          report_month_cur(),
    #                                                                                          math.trunc(round((df7.iloc[
    #                                                                                                                month_index_cur(), i] /
    #                                                                                                            df7.iloc[
    #                                                                                                                month_index_prev(), i]) - 1,
    #                                                                                                           2) * 100),
    #                                                                                          report_month_prev(),
    #                                                                                          (round(df7.iloc[
    #                                                                                                               month_index_cur(), i],
    #                                                                                                           2)),
    #                                                                                          (round(df7.iloc[
    #                                                                                                               month_index_prev(), i],
    #                                                                                                           2))))
    #         else:
    #             st.write('The male {} in {} decreased by {}% compared to {} ({} vs. {})'.format(df7.columns[i][1],
    #                                                                                          report_month_cur(),
    #                                                                                          math.trunc(round((df7.iloc[
    #                                                                                                                month_index_cur(), i] /
    #                                                                                                            df7.iloc[
    #                                                                                                                month_index_prev(), i]) - 1,
    #                                                                                                           2) * 100),
    #                                                                                          report_month_prev(),
    #                                                                                          (round(df7.iloc[
    #                                                                                                               month_index_cur(), i],
    #                                                                                                           2)),
    #                                                                                          (round(df7.iloc[
    #                                                                                                               month_index_prev(), i],
    #                                                                                                           2))))
    #     except:
    #         pass
    #
    # st.write('\n')
    # st.write('MONTH-TO-MONTH FEMALE')
    # for i in range(6, 11):
    #     try:
    #         if (df7.iloc[month_index_cur(), i] / df7.iloc[month_index_prev(), i]) - 1 > 0:
    #             st.write('The female {} in {} increased by {}% compared to {} ({} vs. {})'.format(df7.columns[i][1],
    #                                                                                            report_month_cur(),
    #                                                                                            math.trunc(round((
    #                                                                                                                         df7.iloc[
    #                                                                                                                             month_index_cur(), i] /
    #                                                                                                                         df7.iloc[
    #                                                                                                                             month_index_prev(), i]) - 1,
    #                                                                                                             2) * 100),
    #                                                                                            report_month_prev(),
    #                                                                                            (round(
    #                                                                                                df7.iloc[
    #                                                                                                    month_index_cur(), i],
    #                                                                                                2)),
    #                                                                                            (round(
    #                                                                                                df7.iloc[
    #                                                                                                    month_index_prev(), i],
    #                                                                                                2))))
    #         else:
    #             st.write('The female {} in {} decreased by {}% compared to {} ({} vs. {})'.format(df7.columns[i][1],
    #                                                                                            report_month_cur(),
    #                                                                                            math.trunc(round((
    #                                                                                                                         df7.iloc[
    #                                                                                                                             month_index_cur(), i] /
    #                                                                                                                         df7.iloc[
    #                                                                                                                             month_index_prev(), i]) - 1,
    #                                                                                                             2) * 100),
    #                                                                                            report_month_prev(),
    #                                                                                            math.trunc(round(
    #                                                                                                df7.iloc[
    #                                                                                                    month_index_cur(), i],
    #                                                                                                2)),
    #                                                                                            math.trunc(round(
    #                                                                                                df7.iloc[
    #                                                                                                    month_index_prev(), i],
    #                                                                                                2))))
    #     except:
    #         pass



    det_adp_ytd_pct_change = math.trunc(round((((df7.loc['FY22 Total', ('Total', 'ADP')]) / (df7.loc['FY21 Total', ('Total', 'ADP')]) - 1) * 100), 2))

    if det_admissions_ytd_pct_change > 0:
        st.write('Detention ADP through the first {} months of {} increased by {}% compared to the previous fiscal year-to-date, from {} in {} to {}.'.format(
                                                                                   month_index_cur() + 1,
                                                                                   fy_current,
                                                                                   det_adp_ytd_pct_change,
                                                                                   round(df7.loc['FY21 Total', ('Total', 'ADP')], 1),
                                                                                   fy_previous,
                                                                                   round(df7.loc['FY22 Total', ('Total', 'ADP')], 1)))
    else:
        st.write('Detention ADP through the first {} months of {} decreased by {}% compared to the previous fiscal year-to-date, from {} in {} to {}.'.format(
                                                                                   month_index_cur() + 1,
                                                                                   fy_current,
                                                                                   det_adp_ytd_pct_change,
                                                                                   round(df7.loc['FY21 Total', ('Total', 'ADP')], 1),
                                                                                   fy_previous,
                                                                                   round(df7.loc['FY22 Total', ('Total', 'ADP')], 1)))


    def paragraph_perc(df, col1, col2, dir):
        '''
        enter df and col names and (up or down) for pos. or neg. table
        :param df:
        :param col1:
        :param col2:
        :param dir:
        :return:
        '''
        if dir == 'up':
            up = df[df[col2] > 0]
            p_list = []
            for i, j in zip(up[col1], up[col2]):
                p_list.append('{} (up {}%),'.format(i, round(j * 100)))
            return st.write(' '.join(p_list))

        if dir == 'down':
            down = df[df[col2] < 0]
            p_list = []
            for i, j in zip(down[col1], down[col2]):
                p_list.append('{} (up {}%),'.format(i, round(j * 100)))
            return st.write(' '.join(p_list))



    # Caseloads
    st.markdown("---")
    st.write('\n')
    st.title('***Caseloads MTM***')
    st.write('\n')


    caseload_dict = {}
    cl_name = []
    cl_perc = []

    for i in range(0, 18):
        try:
            if (df8.iloc[month_index_cur(), i] / df8.iloc[month_index_prev(), i]) - 1 > 0:
                   cl_name.append(df8.columns[i])
                   cl_perc.append((df8.iloc[month_index_cur(), i]/df8.iloc[month_index_prev(), i]) - 1)
            else:
                cl_name.append(df8.columns[i])
                cl_perc.append((df8.iloc[month_index_cur(), i]/df8.iloc[month_index_prev(), i]) - 1)

        except:
            pass

    caseload_dict ['Caseload Name'] = cl_name
    caseload_dict ['Caseload Perc. Change (MTM)'] = cl_perc

    # MTM
    cls = pd.DataFrame(caseload_dict).sort_values(by='Caseload Perc. Change (MTM)', ascending=False)

    st.write('The average daily caseloads for the following units increased in {} compared to the previous month:'.format(report_month_cur()))
    # cls_up = cls[cls['Caseload Perc. Change (MTM)'] > 0]
    # cls_p = []
    # for i, j in zip(cls_up['Caseload Name'], cls_up['Caseload Perc. Change (MTM)']):
    #     cls_p.append('{} (up {}%),'.format(i, round(j * 100, 2)))
    #
    # st.write(' '.join(cls_p))
    paragraph_perc(cls, 'Caseload Name', 'Caseload Perc. Change (MTM)', 'up')

    st.write('---')

    st.subheader('Caseloads MTM Percent Change - Increases')
    st.write(cls[cls['Caseload Perc. Change (MTM)'] > 0].reset_index(drop=True).style.format({'Caseload Perc. Change (MTM)': '{:,.2%}'.format}))

    st.subheader('Caseloads MTM Percent Change -  Decreases')
    st.write(cls[cls['Caseload Perc. Change (MTM)'] < 0].sort_values(by='Caseload Perc. Change (MTM)').reset_index(drop=True).style.format({'Caseload Perc. Change (MTM)': '{:,.2%}'.format}))

    st.write('---')

    st.write('\n')
    st.title('***Caseloads YTD***')
    st.write('\n')

    caseload_dict2 = {}
    cl_name2 = []
    cl_perc2 = []

    for i in range(0, 18):
        try:
            if (df8.iloc[-2, i] / df8.iloc[-1, i]) - 1 > 0:
                cl_name2.append(df8.columns[i])
                cl_perc2.append((df8.iloc[-2, i]/df8.iloc[-1, i]) - 1)
            else:
                cl_name2.append(df8.columns[i])
                cl_perc2.append((df8.iloc[-2, i]/df8.iloc[-1, i]) - 1)
        except:
            pass

    caseload_dict2 ['Caseload Name'] = cl_name2
    caseload_dict2 ['Caseload Perc. Change (YTD)'] = cl_perc2

    # YTD
    st.write('The units with a higher average daily officer caseload through {} compared to the previous year-to-date were:'.format(report_month_cur()))

    cls2 = pd.DataFrame(caseload_dict2).sort_values(by='Caseload Perc. Change (YTD)', ascending=False)

    paragraph_perc(cls2, 'Caseload Name', 'Caseload Perc. Change (YTD)', 'up')

    most_decr_unit = \
    cls2[cls2['Caseload Perc. Change (YTD)'] < 0].sort_values(by='Caseload Perc. Change (YTD)').iloc[0].values[0]

    most_decr_unit_perc = \
    cls2[cls2['Caseload Perc. Change (YTD)'] < 0].sort_values(by='Caseload Perc. Change (YTD)').iloc[0].values[1]

    st.write(
    'The unit with the most significant decrease in average daily officer caseload in {} is the {} Unit, down {}% compared to {}.'.format(
        fy_current,
        most_decr_unit,
        abs(round(most_decr_unit_perc * 100)),
        fy_previous
    ))

    st.write('---')

    st.subheader('Caseloads YTD Percent Change - Increases')
    st.write(cls2[cls2['Caseload Perc. Change (YTD)'] > 0].reset_index(drop=True).style.format({'Caseload Perc. Change (YTD)': '{:,.2%}'.format}))

    st.subheader('Caseloads YTD Percent Change -  Decreases')
    st.write(cls2[cls2['Caseload Perc. Change (YTD)'] < 0].sort_values(by='Caseload Perc. Change (YTD)').reset_index(drop=True).style.format({'Caseload Perc. Change (YTD)': '{:,.2%}'.format}))

    st.write('---')

    st.write('\n')
    st.title('***Supervisions***')
    st.write('\n')

    sup_list = []

    if round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Pre-Disposition')] / df9.iloc[month_index_prev(), df9.columns.get_loc('Pre-Disposition')]) - 1)*100) > 0:
        sup_list.append('Compared to the previous month, in {}, the number of those on Pre-Disposition supervision increased by {}%,'.format(
         report_month_cur(),
          abs(round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Pre-Disposition')] / df9.iloc[month_index_prev(), df9.columns.get_loc('Pre-Disposition')]) - 1)*100)
        )))
    else:
        sup_list.append(
            'Compared to the previous month, in {}, the number of those on Pre-Disposition supervision decreased by {}%,'.format(
                report_month_cur(),
                abs(round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Pre-Disposition')] / df9.iloc[
                    month_index_prev(), df9.columns.get_loc('Pre-Disposition')]) - 1) * 100)
                    )))

    if round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Deferred Prosecution')] / df9.iloc[month_index_prev(), df9.columns.get_loc('Deferred Prosecution')]) - 1)*100) > 0:
        sup_list.append('Deferred Prosecution increased by {}%,'.format(
          abs(round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Deferred Prosecution')] / df9.iloc[month_index_prev(), df9.columns.get_loc('Deferred Prosecution')]) - 1)*100)
        )))
    else:
        sup_list.append(
            'Deferred Prosecution decreased by {}%,'.format(
                abs(round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Deferred Prosecution')] / df9.iloc[
                    month_index_prev(), df9.columns.get_loc('Deferred Prosecution')]) - 1) * 100)
                    )))

    if round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Adjudication Probation (Non-ISP)')] / df9.iloc[month_index_prev(), df9.columns.get_loc('Adjudication Probation (Non-ISP)')]) - 1)*100) > 0:
        sup_list.append('non-ISP Probation increased by {}%,'.format(
          abs(round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Adjudication Probation (Non-ISP)')] / df9.iloc[month_index_prev(), df9.columns.get_loc('Adjudication Probation (Non-ISP)')]) - 1)*100)
        )))
    else:
        sup_list.append('non-ISP Probation decreased by {}%,'.format(
                abs(round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Adjudication Probation (Non-ISP)')] / df9.iloc[
                    month_index_prev(), df9.columns.get_loc('Adjudication Probation (Non-ISP)')]) - 1) * 100)
                    )))

    if round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Adjudication Probation (ISP)')] / df9.iloc[month_index_prev(), df9.columns.get_loc('Adjudication Probation (ISP)')]) - 1)*100) > 0:
        sup_list.append('and ISP Probation increased by {}%.'.format(
          abs(round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Adjudication Probation (ISP)')] / df9.iloc[month_index_prev(), df9.columns.get_loc('Adjudication Probation (ISP)')]) - 1)*100)
        )))
    else:
        sup_list.append('and ISP Probation decreased by {}%.'.format(
                abs(round(((df9.iloc[month_index_cur(), df9.columns.get_loc('Adjudication Probation (ISP)')] / df9.iloc[
                    month_index_prev(), df9.columns.get_loc('Adjudication Probation (ISP)')]) - 1) * 100)
                    )))


    st.write(' '.join(sup_list))


    # Supervision YTD text
    sup_list2 = []
    if month_index_cur() == 11:
        sup_list2.append('When looking at the entire fiscal year,')
    else:
        sup_list2.append('Through the first {} months of {}'.format(month_index_cur()+1, fy_current ))

    if round(((df9.iloc[-2, df9.columns.get_loc('Pre-Disposition')] / df9.iloc[-1, df9.columns.get_loc('Pre-Disposition')]) - 1) * 100) > 0:
        sup_list2.append('the average daily number of youths on Pre-Disposition supervision increased by {}%,'.format(
            abs(round(((df9.iloc[-2, df9.columns.get_loc('Pre-Disposition')] / df9.iloc[
                -1, df9.columns.get_loc('Pre-Disposition')]) - 1) * 100))))
    else:
        sup_list2.append('the average daily number of youths on Pre-Disposition supervision decreased by {}%,'.format(
            abs(round(((df9.iloc[-2, df9.columns.get_loc('Pre-Disposition')] / df9.iloc[
                -1, df9.columns.get_loc('Pre-Disposition')]) - 1) * 100))))

    if round(((df9.iloc[-2, df9.columns.get_loc('Deferred Prosecution')] / df9.iloc[ -1, df9.columns.get_loc('Deferred Prosecution')]) - 1) * 100) > 0:
        sup_list2.append('Deferred Prosecution increased by {}%,'.format(
            abs(round(((df9.iloc[-2, df9.columns.get_loc('Deferred Prosecution')] / df9.iloc[
                -1, df9.columns.get_loc('Deferred Prosecution')]) - 1) * 100))
        ))
    else:
        sup_list2.append('Deferred Prosecution decreased by {}%,'.format(
            abs(round(((df9.iloc[-2, df9.columns.get_loc('Deferred Prosecution')] / df9.iloc[
                -1, df9.columns.get_loc('Deferred Prosecution')]) - 1) * 100))
        ))

    if round(((df9.iloc[-2, df9.columns.get_loc('Adjudication Probation (Non-ISP)')] / df9.iloc[-1, df9.columns.get_loc('Adjudication Probation (Non-ISP)')]) - 1) * 100) > 0:
        sup_list2.append('non-ISP Probation increased by {}%,'.format(
            abs(round(((df9.iloc[-2, df9.columns.get_loc('Adjudication Probation (Non-ISP)')] / df9.iloc[
                -1, df9.columns.get_loc('Adjudication Probation (Non-ISP)')]) - 1) * 100))
        ))
    else:
        sup_list2.append('non-ISP Probation decreased by {}%,'.format(
            abs(round(((df9.iloc[-2, df9.columns.get_loc('Adjudication Probation (Non-ISP)')] / df9.iloc[
                -1, df9.columns.get_loc('Adjudication Probation (Non-ISP)')]) - 1) * 100))
        ))

    if round(((df9.iloc[-2, df9.columns.get_loc('Adjudication Probation (ISP)')] / df9.iloc[-1, df9.columns.get_loc('Adjudication Probation (ISP)')]) - 1) * 100) > 0:
        sup_list2.append('and ISP Probation increased by {}%.'.format(
            abs(round(((df9.iloc[-2, df9.columns.get_loc('Adjudication Probation (ISP)')] / df9.iloc[
                -1, df9.columns.get_loc('Adjudication Probation (ISP)')]) - 1) * 100))
        ))
    else:
        sup_list2.append('and ISP Probation decreased by {}%.'.format(
            abs(round(((df9.iloc[-2, df9.columns.get_loc('Adjudication Probation (ISP)')] / df9.iloc[
                -1, df9.columns.get_loc('Adjudication Probation (ISP)')]) - 1) * 100))
        ))

    st.write(' '.join(sup_list2))


    st.write('---')
    st.subheader('***Supervision MTM***')

    for i in range(0, 6):
        try:
            if (df9.iloc[month_index_cur(), i] / df9.iloc[month_index_prev(), i]) - 1 > 0:
                st.write(
                    'The average daily number of youths on {} Supervision in {} increased by {}% compared to {}, ({} vs. {})'.format(
                        df9.columns[i],
                        report_month_cur(),
                        math.trunc(round((df9.iloc[month_index_cur(), i] / df9.iloc[month_index_prev(), i]) - 1, 2) * 100),
                        report_month_prev(),
                        math.trunc(round(df9.iloc[month_index_cur(), i], 2)),
                        math.trunc(round(df9.iloc[month_index_prev(), i], 2))))
            else:
                st.write(
                    'The average daily number of youths on {} Supervision in {} decreased by {}% compared to {}, ({} vs. {})'.format(
                        df9.columns[i],
                        report_month_cur(),
                        math.trunc(round((df9.iloc[month_index_cur(), i] / df9.iloc[month_index_prev(), i]) - 1, 2) * 100),
                        report_month_prev(),
                        math.trunc(round(df9.iloc[month_index_cur(), i], 2)),
                        math.trunc(round(df9.iloc[month_index_prev(), i], 2))))
        except:
            pass

    st.write('\n')
    st.subheader('***Supervision YTD***')
    st.write('\n')

    for i in range(0, 6):
        try:
            if (df9.iloc[-2, i] / df9.iloc[-1, i]) - 1 > 0:
                st.write(
                    'The average daily number of youths on {} Supervision increased by {}% through {} {} YTD, compared to {} YTD ({} vs. {})'.format(
                        df9.columns[i],
                        math.trunc(round((df9.iloc[-2, i] / df9.iloc[-1, i]) - 1, 2) * 100),
                        report_month_cur(),
                        fy_current,
                        fy_previous,
                        math.trunc(round(df9.iloc[-2, i], 2)),
                        math.trunc(round(df9.iloc[-1, i], 2))))
            else:
                st.write(
                    'The average daily number of youths on {} Supervision decreased by {}% through {} {} YTD, compared to {} YTD ({} vs. {})'.format(
                        df9.columns[i],
                        math.trunc(round((df9.iloc[-2, i] / df9.iloc[-1, i]) - 1, 2) * 100),
                        report_month_cur(),
                        fy_current,
                        fy_previous,
                        math.trunc(round(df9.iloc[-2, i], 2)),
                        math.trunc(round(df9.iloc[-1, i], 2))))
        except:
            pass



    st.markdown("---")
    st.write('\n')
    st.title('***Internal Placement***')
    st.subheader('ADP MTM')
    st.write('\n')

    int_pl_dict = {}
    pl_name = []
    pl_perc = []

    for i in range(7, 107, 9):
        try:
            if (df10.iloc[month_index_cur(), i] / df10.iloc[month_index_prev(), i]) - 1 > 0:
                pl_name.append(df10.columns[i])
                pl_perc.append((df10.iloc[month_index_cur(), i]/df10.iloc[month_index_prev(), i]) - 1)

            else:
                pl_name.append(df10.columns[i])
                pl_perc.append((df10.iloc[month_index_cur(), i]/df10.iloc[month_index_prev(), i]) - 1)

        except:
            pass

    int_pl_dict ['Placement'] = pl_name
    int_pl_dict ['Placement Perc. Change (MTM)'] = pl_perc

    # MTM
    int_pl = pd.DataFrame(int_pl_dict).sort_values(by='Placement Perc. Change (MTM)', ascending=False)
    int_pl_up = int_pl[int_pl['Placement Perc. Change (MTM)'] > 0]
    int_pl_up_p = []

    int_pl_up_p.append('In {}, the following facilities had an increase in their ADP compared to the previous month:'.format(report_month_cur()))

    for i, j in zip(int_pl_up['Placement'], int_pl_up['Placement Perc. Change (MTM)']):
        int_pl_up_p.append('{} (up {}%),'.format(i[:-5], round(j * 100)))

    st.write(' '.join(int_pl_up_p))

    int_pl_down = int_pl[int_pl['Placement Perc. Change (MTM)'] < 0].sort_values('Placement Perc. Change (MTM)')
    int_pl_down['Placement Perc. Change (MTM)'] = int_pl_down['Placement Perc. Change (MTM)'].abs()
    int_pl_down_p = []

    int_pl_down_p.append('The following facilities saw a decrease in their ADP compared to the previous month:')
    for i, j in zip(int_pl_down['Placement'], int_pl_down['Placement Perc. Change (MTM)']):
        int_pl_down_p.append('{} (down {}%),'.format(i[:-5], round(j * 100)))

    st.write(' '.join(int_pl_down_p))
    st.write('---')


    st.subheader('Internal Placement ADP MTM - Increases')
    st.dataframe(int_pl[int_pl['Placement Perc. Change (MTM)'] > 0].reset_index(drop=True).style.format({'Placement Perc. Change (MTM)': '{:,.2%}'.format}))
    st.subheader('Internal Placement ADP MTM - Decreases')
    st.write(int_pl[int_pl['Placement Perc. Change (MTM)'] < 0].sort_values(by='Placement Perc. Change (MTM)').reset_index(drop=True).style.format({'Placement Perc. Change (MTM)': '{:,.2%}'.format}))
    st.write('---')


    st.write('\n')
    st.subheader('***Internal Placement ADP YTD***')
    st.write('\n')

    int_pl_dict2 = {}
    pl_name2 = []
    pl_perc2 = []

    for i in range(7, 107, 9):
        try:
            if (df10.iloc[-2, i] / df10.iloc[-1, i]) - 1 > 0:
                pl_name2.append(df10.columns[i])
                pl_perc2.append((df10.iloc[-2, i]/df10.iloc[-1, i]) - 1)

            else:
                pl_name2.append(df10.columns[i])
                pl_perc2.append((df10.iloc[-2, i]/df10.iloc[-1, i]) - 1)

        except:
            pass

    int_pl_dict2 ['Placement'] = pl_name2
    int_pl_dict2 ['Placement Perc. Change (YTD)'] = pl_perc2

    # YTD
    int_pl2 = pd.DataFrame(int_pl_dict2).sort_values(by='Placement Perc. Change (YTD)', ascending=False)
    int_pl_up_p2 = []

    if month_index_cur() == 11:
        int_pl_up_p2.append('When comparing each facility’s {} ADP to that of the previous fiscal year, the following facilities had an increase:'.format(fy_current))
    else:
        int_pl_up_p2.append('When comparing each facility’s ADP for the first {} months of {} to the same months of the previous fiscal year, the following facilities had an increase:'.format(month_index_cur()+1, fy_current))

    int_pl_up2 = int_pl2[int_pl2['Placement Perc. Change (YTD)'] > 0]
    for i, j in zip(int_pl_up2['Placement'], int_pl_up2['Placement Perc. Change (YTD)']):
        int_pl_up_p2.append('{} (up {}%),'.format(i[:-5], round(j * 100)))

    st.write(' '.join(int_pl_up_p2))

    # Internal Placement YTD decreases
    int_pl_down_p2 = []

    if month_index_cur() == 11:
        int_pl_down_p2.append('Compared to {},'.format(fy_previous))
    else:
        int_pl_down_p2.append('Compared to the same months of the previous fiscal year,')


    int_pl_down2 = int_pl2[int_pl2['Placement Perc. Change (YTD)'] < 0]
    for i, j in zip(int_pl_down2['Placement'], int_pl_down2['Placement Perc. Change (YTD)']):
        int_pl_down_p2.append('{} (down {}%),'.format(i[:-5], abs(round(j * 100))))

    st.write(' '.join(int_pl_down_p2))

    st.write('---')
    st.subheader('Internal Placement ADP YTD - Increases')
    st.write(int_pl2[int_pl2['Placement Perc. Change (YTD)'] > 0].reset_index(drop=True).style.format({'Placement Perc. Change (YTD)': '{:,.2%}'.format}))
    st.subheader('Internal Placement ADP YTD - Decreases')
    st.write(int_pl2[int_pl2['Placement Perc. Change (YTD)'] < 0].sort_values(by='Placement Perc. Change (YTD)').reset_index(drop=True).style.format({'Placement Perc. Change (YTD)': '{:,.2%}'.format}))



    st.markdown("---")
    st.write('\n')
    st.title('***Contract Placement***')
    st.write('\n')

    con_place_list = []

    con_place_list.append('{} youth were served at contract placement facilities in {}, including {} admissions during {}.'.format(df11.iloc[month_index_cur(), 0],
                                                                                                               report_month_cur(),
                                                                                                               df11.iloc[month_index_cur(), 1],
                                                                                                               report_month_cur()
                                                                                                               ))

    con_place_list.append('Specifically,')
    new_youth_plc = df11[df11.columns[df11.columns.str.contains('Youth Served')]].iloc[month_index_prev():month_index_cur() + 1, 1:].diff().dropna().T
    new_youth_plc = new_youth_plc[new_youth_plc.SEP > 0]

    for index, value in zip(new_youth_plc.index, new_youth_plc.values.flatten()):
        con_place_list.append('{} youth was admitted to {}, '.format(value, index[:-14]))

    con_place_list.append('There were {} exits from contract placement facilities during {}.'.format(df11.iloc[month_index_cur(), 2], report_month_cur()))

    st.write(' '.join(con_place_list))

    con_place_list2 = []

    if month_index_cur() == 11:
        con_place_list2.append('The FY2022 contract placement ADP'.format(fy_previous))
    else:
        con_place_list2.append('The contract placement YTD ADP through {}'.format(report_month_cur()))

    if df11['All External Facilities: ADP'][-2] > df11['All External Facilities: ADP'][-1]:
        con_place_list2.append(
            'was {}, {}% above that of the previous fiscal year’s first {} months ({}).'.format(
                round(df11['All External Facilities: ADP'][-2], 1),
                int(((df11['All External Facilities: ADP'][-2] / df11['All External Facilities: ADP'][-1]) - 1) * 100),
                month_index_cur() + 1,
                round(df11['All External Facilities: ADP'][-1], 1)))
    else:
        con_place_list2.append(
            'was {}, {}% below that of the previous fiscal year’s first {} months ({}).'.format(
                round(df11['All External Facilities: ADP'][-2], 1),
                int(((df11['All External Facilities: ADP'][-2] / df11['All External Facilities: ADP'][-1]) - 1) * 100),
                month_index_cur() + 1,
                round(df11['All External Facilities: ADP'][-1], 1)))

    st.write(' '.join(con_place_list2))

    st.markdown('---')
    st.write('\n')
    st.title('***Psych/Clinical Services***')
    st.write('\n')

    psych_list = []

    if (df12.iloc[month_index_cur(), -1] / df12.iloc[month_index_prev(), -1]) - 1 > 0:
        psych_list.append(
            '{} Psychological Services Referrals were made in {}, a {}% increase compared to  {} ({} vs. {}).'.format(
                df12.iloc[month_index_cur(), -1],
                report_month_cur(),
                math.trunc(round((df12.iloc[month_index_cur(), -1] / df12.iloc[month_index_prev(), -1]) - 1, 2) * 100),
                report_month_prev(),
                math.trunc(round(df12.iloc[month_index_cur(), -1])),
                math.trunc(round(df12.iloc[month_index_prev(), -1]))))
    else:
        psych_list.append('({}) Psychological Services Referrals were made in {}, a {}% decrease compared to {} ({} vs. {})'.format(
            df12.iloc[month_index_cur(), -1],
            report_month_cur(),
            math.trunc(round((df12.iloc[month_index_cur(), -1] / df12.iloc[month_index_prev(), -1]) - 1, 2) * 100),
            report_month_prev(),
            math.trunc(round(df12.iloc[month_index_cur(), -1])),
            math.trunc(round(df12.iloc[month_index_prev(), -1]))))

    psych_list.append('The number of Psychological Service Referrals made')
    if month_index_cur() == 11:
        psych_list.append('in {}'.format(fy_current))
    else:
        psych_list.append('through the first {} months of {}'.format(month_index_cur()+1, fy_current))

    if (df12.iloc[-2, -1] / df12.iloc[-1, -1]) - 1 > 0:
        psych_list.append(
            ' are up {}% compared to the same months in {}.'.format(
                round_pct_change(df12.iloc[-2, -1], df12.iloc[-1, -1]),
                fy_previous))
    else:
        psych_list.append(
            'are down {}% compared to the same months in {}.'.format(
                round_pct_change(df12.iloc[-2, -1], df12.iloc[-1, -1]),
                fy_previous))

    st.write(' '.join(psych_list))


    psych_list2 = []
    if round_pct_change(df13.iloc[month_index_cur(), df13.columns.get_loc('Total')], df13.iloc[month_index_prev(), df13.columns.get_loc('Total')]) > 0:
        psych_list2.append(
            'The number of Behavioral Health Services Referrals made during {} increased by {}% compared to the previous month.'.format(
                report_month_cur(),
                abs(round_pct_change(df13.iloc[month_index_cur(), df13.columns.get_loc('Total')],
                                     df13.iloc[month_index_prev(), df13.columns.get_loc('Total')]))
            ))
    else:
        psych_list2.append(
            'The number of Behavioral Health Services Referrals made during {} decreased by {}% compared to the previous month.'.format(
                report_month_cur(),
                abs(round_pct_change(df13.iloc[month_index_cur(), df13.columns.get_loc('Total')],
                                     df13.iloc[month_index_prev(), df13.columns.get_loc('Total')]))
            ))

    st.write(' '.join(psych_list2))


    st.write('---')
    st.write('\n')
    st.subheader('***Psychological Services Referrals YTD***')

    st.write('***During the first {} months of {} YTD:***'.format(month_index_cur() + 1, fy_current))

    psych_ytd_dict = {}
    psych_names = []
    psych_chg = []
    psych_prev = []
    psych_cur = []

    # for i in range(0, df12.shape[1]):
    #     try:
    #         if (df12.iloc[-2, i] / df12.iloc[-1, i]) - 1 > 0:
    #             st.write(
    #                 '{}: {}% increase ({}: {} | {}: {})'.format(
    #                     df12.columns[i],
    #                     round_pct_change(df12.iloc[-2, i], df12.iloc[-1, i]),
    #                     fy_previous,
    #                     round(df12.iloc[-1, i]),
    #                     fy_current,
    #                     round(df12.iloc[-2, i])
    #                     ))
    #         else:
    #             st.write(
    #                 '{}: {}% decrease ({}: {} | {}: {})'.format(
    #                     df12.columns[i],
    #                     round_pct_change(df12.iloc[-2, i], df12.iloc[-1, i]),
    #                     fy_previous,
    #                     round(df12.iloc[-1, i]),
    #                     fy_current,
    #                     round(df12.iloc[-2, i])
    #                     ))
    #     except ZeroDivisionError:
    #         pass

    for i in range(0, df12.shape[1]):
        try:
            if (df12.iloc[-2, i] / df12.iloc[-1, i]) - 1 > 0:
                psych_names.append(df12.columns[i])
                psych_chg.append('{}% increase'.format(round_pct_change(df12.iloc[-2, i], df12.iloc[-1, i])))
                psych_prev.append(round(df12.iloc[-1, i]))
                psych_cur.append(round(df12.iloc[-2, i]))

            else:
                psych_names.append(df12.columns[i])
                psych_chg.append('{}% decrease'.format(abs(round_pct_change(df12.iloc[-2, i], df12.iloc[-1, i]))))
                psych_prev.append(round(df12.iloc[-1, i]))
                psych_cur.append(round(df12.iloc[-2, i]))
        except ZeroDivisionError:
            pass

    psych_ytd_dict['Service     '] = psych_names
    psych_ytd_dict['Percent Change'] = psych_chg
    psych_ytd_dict['{}'.format(fy_previous)] = psych_prev
    psych_ytd_dict['{}'.format(fy_current)] = psych_cur

    psych_df = pd.DataFrame(psych_ytd_dict)
    st.write(psych_df)

    st.write('---')
    st.subheader('***Behavioral Health Services Referrals MTM***')

    bh_mtm_dict = {}
    bh_mtm_name = []
    bh_mtm_chg = []
    bh_mtm_prev = []
    bh_mtm_cur = []

    for i in range(0, df13.shape[1]):
        try:
            if (df13.iloc[month_index_cur(), i] / df13.iloc[month_index_prev(), i]) - 1 > 0:
                bh_mtm_name.append(df13.columns[i])
                bh_mtm_chg.append('{}% increase'.format(round_pct_change(df13.iloc[month_index_cur(), i], df13.iloc[month_index_prev(), i])))
                bh_mtm_prev.append(round(df13.iloc[month_index_prev(), i]))
                bh_mtm_cur.append(round(df13.iloc[month_index_cur(), i]))
            else:
                bh_mtm_name.append(df13.columns[i])
                bh_mtm_chg.append('{}% decrease'.format(abs(round_pct_change(df13.iloc[month_index_cur(), i], df13.iloc[month_index_prev(), i]))))
                bh_mtm_prev.append(round(df13.iloc[month_index_prev(), i]))
                bh_mtm_cur.append(round(df13.iloc[month_index_cur(), i]))
        except ZeroDivisionError:
            pass

    bh_mtm_dict['Service'] = bh_mtm_name
    bh_mtm_dict['Percent Change'] = bh_mtm_chg
    bh_mtm_dict['{}'.format(report_month_prev())] = bh_mtm_prev
    bh_mtm_dict['{}'.format(report_month_cur())] = bh_mtm_cur

    st.dataframe(pd.DataFrame(bh_mtm_dict))


    st.write('\n')
    st.subheader('***Behavioral Health Services Referrals YTD***')

    bh_ytd_dict = {}
    bh_ytd_name = []
    bh_ytd_chg = []
    bh_ytd_prev = []
    bh_ytd_cur = []

    for i in range(0, df13.shape[1]):
        try:
            if (df13.iloc[-2, i] / df13.iloc[-1, i]) - 1 > 0:
                bh_ytd_name.append(df13.columns[i])
                bh_ytd_chg.append('{}% increase'.format(round_pct_change(df13.iloc[-2, i], df13.iloc[-1, i])))
                bh_ytd_prev.append(round(df13.iloc[-1, i]))
                bh_ytd_cur.append(round(df13.iloc[-2, i]))
            else:
                bh_ytd_name.append(df13.columns[i])
                bh_ytd_chg.append('{}% decrease'.format(abs(round_pct_change(df13.iloc[-2, i], df13.iloc[-1, i]))))
                bh_ytd_prev.append(round(df13.iloc[-1, i]))
                bh_ytd_cur.append(round(df13.iloc[-2, i]))
        except ZeroDivisionError:
            pass

    bh_ytd_dict['Service'] = bh_ytd_name
    bh_ytd_dict['Percent Change'] = bh_ytd_chg
    bh_ytd_dict['{}'.format(fy_previous)] = bh_ytd_prev
    bh_ytd_dict['{}'.format(fy_current)] = bh_ytd_cur

    st.dataframe(pd.DataFrame(bh_ytd_dict))


    # for i in range(0, df13.shape[1]):
    #     try:
    #
    #         if (df13.iloc[-2, i] / df13.iloc[-1, i]) - 1 > 0:
    #             st.write(
    #                 '{} Referrals made through {} {} YTD were up {}% compared to {} YTD ({} vs. {}).'.format(
    #                     df13.columns[i],
    #                     report_month_cur(),
    #                     fy_current,
    #                     math.trunc(round((df13.iloc[-2, i] / df13.iloc[-1, i]) - 1, 2) * 100),
    #                     fy_previous,
    #                     math.trunc(round(df13.iloc[-2, i], 2)),
    #                     math.trunc(round(df13.iloc[-1, i], 2))))
    #         else:
    #             st.write(
    #                 '{} Referrals made through {} {} YTD were down {}% compared to {} YTD ({} vs. {}).'.format(
    #                     df13.columns[i],
    #                     report_month_cur(),
    #                     fy_current,
    #                     math.trunc(round((df13.iloc[-2, i] / df13.iloc[-1, i]) - 1, 2) * 100),
    #                     fy_previous,
    #                     math.trunc(round(df13.iloc[-2, i], 2)),
    #                     math.trunc(round(df13.iloc[-1, i], 2))))
    #     except ZeroDivisionError:
    #         pass

    st.write('\n')
    st.subheader('***Clinical Service Referral Outcomes YTD***')
    st.write(
        'Through the first {} months of {}, {}% of all Psychological Services Referrals had a completed outcome,'.format(
            month_index_cur() + 1,
            fy_current,
            math.trunc(round(df14.iloc[-2, 0], 2) * 100),
            ))
    st.write(
        'Through the first {} months of {}, {}% of all Psychological Services Referrals had a completed outcome,'.format(
            month_index_cur() + 1,
            fy_previous,
            math.trunc(round(df14.iloc[-1, 0], 2) * 100),
            ))
    st.write(
        'Through the first {} months of {}, {}% of all Behavioral Health Services Referrals had a completed outcome,'.format(
            month_index_cur() + 1,
            fy_current,
            math.trunc(round(df14.iloc[-2, 1], 2) * 100),
            ))
    st.write(
        'Through the first {} months of {}, {}% of all Behavioral Health Services Referrals had a completed outcome,'.format(
            month_index_cur() + 1,
            fy_previous,
            math.trunc(round(df14.iloc[-1, 1], 2) * 100),
            ))



    st.markdown("---")
    st.title('***Education***')

    st.write('The Dallas County JJAEP had {} admissions in {}.'.format(int(df15.iloc[month_index_cur(), 4]), report_month_cur()))

    st.write('Of the youth served, {}% were Mandatory admissions, {}% were Discretionary, and {}% was Other.'.format(
        round((df15.iloc[month_index_cur(), 1] / df15.iloc[month_index_cur(), 0]) * 100),
        round((df15.iloc[month_index_cur(), 2] / df15.iloc[month_index_cur(), 0]) * 100),
        round((df15.iloc[month_index_cur(), 3] / df15.iloc[month_index_cur(), 0]) * 100)))

    st.write('There were {} total exits from JJAEP in {}, {} of whom discharged successfully, {} unsuccessfully, and {} other.'.format(
            int(df15.iloc[month_index_cur(), 5]),
            report_month_cur(),
            int(df15.iloc[month_index_cur(), 6]),
            int(df15.iloc[month_index_cur(), 7]),
            int(df15.iloc[month_index_cur(), 8])
            ))

    st.write('***[\* INSERT UNSUCCESSFUL EXITS REASONS HERE \*]***')

    st.write('\n')
    st.write('Through {} fiscal YTD: '.format(report_month_cur()))

    for i in range(0, 13):
        try:

            if (df15.iloc[-2, i] / df15.iloc[-1, i]) - 1 > 0:
                st.write(
                    '{}: {}% increase ({}: {} | {}: {})'.format(
                        df15.columns[i],
                        round_pct_change(df15.iloc[-2, i], df15.iloc[-1, i]),
                        fy_previous,
                        round(df15.iloc[-1, i]),
                        fy_current,
                        round(df15.iloc[-2, i]),
                    ))
            else:
                st.write(
                    '{}: {}% decrease ({}: {} | {}: {})'.format(
                        df15.columns[i],
                        abs(round_pct_change(df15.iloc[-2, i], df15.iloc[-1, i])),
                        fy_previous,
                        round(df15.iloc[-1, i]),
                        fy_current,
                        round(df15.iloc[-2, i]),
                    ))
        except ZeroDivisionError:
            pass





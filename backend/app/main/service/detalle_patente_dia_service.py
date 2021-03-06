import uuid
import datetime

from app.main import db
from app.main.model.detalle_patente_dia import DetallePatenteDia
from app.main.model.ranking import RankingEntry
import shap
import joblib
import pandas as pd
import base64
from io import BytesIO
import xgboost as xgb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import folium
import numpy as np

ranker_features = [
 'dt_dayofweek0',
 'dt_dayofweek1',
 'dt_dayofweek2',
 'dt_dayofweek3',
 'dt_dayofweek4',
 'dt_dayofweek5',
 'dt_dayofweek6',
 'dt_month1',
 'dt_month2',
 'dt_month3',
 'dt_month4',
 'dt_month5',
 'dt_month6',
 'dt_month7',
 'dt_month8',
 'dt_month11',
 'dt_month12',
 'day_minus_one_risk_index_w',
 'day_minus_one_risk_index',
 'day_minus_one_relevance',
 'day_minus_one_sum_distance',
 'day_minus_one_min_distance',
 'day_minus_one_max_distance',
 'day_minus_one_mean_distance',
 'day_minus_one_std_distance',
 'day_minus_one_min_speed',
 'day_minus_one_max_speed',
 'day_minus_one_mean_speed',
 'day_minus_one_std_speed',
 'day_minus_one_prealert_low_count',
 'day_minus_one_prealert_mid_count',
 'day_minus_one_prealert_high_count',
 'day_minus_one_alert_low_count',
 'day_minus_one_alert_mid_count',
 'day_minus_one_alert_high_count',
 'day_minus_one_alert_speed_limit_low_count',
 'day_minus_one_alert_speed_limit_mid_count',
 'day_minus_one_alert_speed_limit_high_count',
 'day_minus_one_no_alert_flag',
 'day_minus_one_pre_alert_count_by_100km',
 'day_minus_one_alert_count_by_100km',
 'day_minus_one_speed_limit_alert_count_by_100km',
 'day_minus_one_mixed_alert_count_by_100km',
 'day_minus_one_no_alert_count_by_100km',
 'day_minus_one_max_speed_over_weekly_max',
 'day_minus_one_speed_departure_from_weekly_mean',
 'day_minus_one_std_speed_departure_from_weekly_mean',
 'day_minus_one_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_one_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_one_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_one_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_two_risk_index_w',
 'day_minus_two_risk_index',
 'day_minus_two_relevance',
 'day_minus_two_sum_distance',
 'day_minus_two_min_distance',
 'day_minus_two_max_distance',
 'day_minus_two_mean_distance',
 'day_minus_two_std_distance',
 'day_minus_two_min_speed',
 'day_minus_two_max_speed',
 'day_minus_two_mean_speed',
 'day_minus_two_std_speed',
 'day_minus_two_prealert_low_count',
 'day_minus_two_prealert_mid_count',
 'day_minus_two_prealert_high_count',
 'day_minus_two_alert_low_count',
 'day_minus_two_alert_mid_count',
 'day_minus_two_alert_high_count',
 'day_minus_two_alert_speed_limit_low_count',
 'day_minus_two_alert_speed_limit_mid_count',
 'day_minus_two_alert_speed_limit_high_count',
 'day_minus_two_no_alert_flag',
 'day_minus_two_pre_alert_count_by_100km',
 'day_minus_two_alert_count_by_100km',
 'day_minus_two_speed_limit_alert_count_by_100km',
 'day_minus_two_mixed_alert_count_by_100km',
 'day_minus_two_no_alert_count_by_100km',
 'day_minus_two_max_speed_over_weekly_max',
 'day_minus_two_speed_departure_from_weekly_mean',
 'day_minus_two_std_speed_departure_from_weekly_mean',
 'day_minus_two_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_two_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_two_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_two_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_three_risk_index_w',
 'day_minus_three_risk_index',
 'day_minus_three_relevance',
 'day_minus_three_sum_distance',
 'day_minus_three_min_distance',
 'day_minus_three_max_distance',
 'day_minus_three_mean_distance',
 'day_minus_three_std_distance',
 'day_minus_three_min_speed',
 'day_minus_three_max_speed',
 'day_minus_three_mean_speed',
 'day_minus_three_std_speed',
 'day_minus_three_prealert_low_count',
 'day_minus_three_prealert_mid_count',
 'day_minus_three_prealert_high_count',
 'day_minus_three_alert_low_count',
 'day_minus_three_alert_mid_count',
 'day_minus_three_alert_high_count',
 'day_minus_three_alert_speed_limit_low_count',
 'day_minus_three_alert_speed_limit_mid_count',
 'day_minus_three_alert_speed_limit_high_count',
 'day_minus_three_no_alert_flag',
 'day_minus_three_pre_alert_count_by_100km',
 'day_minus_three_alert_count_by_100km',
 'day_minus_three_speed_limit_alert_count_by_100km',
 'day_minus_three_mixed_alert_count_by_100km',
 'day_minus_three_no_alert_count_by_100km',
 'day_minus_three_max_speed_over_weekly_max',
 'day_minus_three_speed_departure_from_weekly_mean',
 'day_minus_three_std_speed_departure_from_weekly_mean',
 'day_minus_three_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_three_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_three_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_three_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_four_risk_index_w',
 'day_minus_four_risk_index',
 'day_minus_four_relevance',
 'day_minus_four_sum_distance',
 'day_minus_four_min_distance',
 'day_minus_four_max_distance',
 'day_minus_four_mean_distance',
 'day_minus_four_std_distance',
 'day_minus_four_min_speed',
 'day_minus_four_max_speed',
 'day_minus_four_mean_speed',
 'day_minus_four_std_speed',
 'day_minus_four_prealert_low_count',
 'day_minus_four_prealert_mid_count',
 'day_minus_four_prealert_high_count',
 'day_minus_four_alert_low_count',
 'day_minus_four_alert_mid_count',
 'day_minus_four_alert_high_count',
 'day_minus_four_alert_speed_limit_low_count',
 'day_minus_four_alert_speed_limit_mid_count',
 'day_minus_four_alert_speed_limit_high_count',
 'day_minus_four_no_alert_flag',
 'day_minus_four_pre_alert_count_by_100km',
 'day_minus_four_alert_count_by_100km',
 'day_minus_four_speed_limit_alert_count_by_100km',
 'day_minus_four_mixed_alert_count_by_100km',
 'day_minus_four_no_alert_count_by_100km',
 'day_minus_four_max_speed_over_weekly_max',
 'day_minus_four_speed_departure_from_weekly_mean',
 'day_minus_four_std_speed_departure_from_weekly_mean',
 'day_minus_four_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_four_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_four_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_four_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_five_risk_index_w',
 'day_minus_five_risk_index',
 'day_minus_five_relevance',
 'day_minus_five_sum_distance',
 'day_minus_five_min_distance',
 'day_minus_five_max_distance',
 'day_minus_five_mean_distance',
 'day_minus_five_std_distance',
 'day_minus_five_min_speed',
 'day_minus_five_max_speed',
 'day_minus_five_mean_speed',
 'day_minus_five_std_speed',
 'day_minus_five_prealert_low_count',
 'day_minus_five_prealert_mid_count',
 'day_minus_five_prealert_high_count',
 'day_minus_five_alert_low_count',
 'day_minus_five_alert_mid_count',
 'day_minus_five_alert_high_count',
 'day_minus_five_alert_speed_limit_low_count',
 'day_minus_five_alert_speed_limit_mid_count',
 'day_minus_five_alert_speed_limit_high_count',
 'day_minus_five_no_alert_flag',
 'day_minus_five_pre_alert_count_by_100km',
 'day_minus_five_alert_count_by_100km',
 'day_minus_five_speed_limit_alert_count_by_100km',
 'day_minus_five_mixed_alert_count_by_100km',
 'day_minus_five_no_alert_count_by_100km',
 'day_minus_five_max_speed_over_weekly_max',
 'day_minus_five_speed_departure_from_weekly_mean',
 'day_minus_five_std_speed_departure_from_weekly_mean',
 'day_minus_five_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_five_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_five_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_five_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_six_risk_index_w',
 'day_minus_six_risk_index',
 'day_minus_six_relevance',
 'day_minus_six_sum_distance',
 'day_minus_six_min_distance',
 'day_minus_six_max_distance',
 'day_minus_six_mean_distance',
 'day_minus_six_std_distance',
 'day_minus_six_min_speed',
 'day_minus_six_max_speed',
 'day_minus_six_mean_speed',
 'day_minus_six_std_speed',
 'day_minus_six_prealert_low_count',
 'day_minus_six_prealert_mid_count',
 'day_minus_six_prealert_high_count',
 'day_minus_six_alert_low_count',
 'day_minus_six_alert_mid_count',
 'day_minus_six_alert_high_count',
 'day_minus_six_alert_speed_limit_low_count',
 'day_minus_six_alert_speed_limit_mid_count',
 'day_minus_six_alert_speed_limit_high_count',
 'day_minus_six_no_alert_flag',
 'day_minus_six_pre_alert_count_by_100km',
 'day_minus_six_alert_count_by_100km',
 'day_minus_six_speed_limit_alert_count_by_100km',
 'day_minus_six_mixed_alert_count_by_100km',
 'day_minus_six_no_alert_count_by_100km',
 'day_minus_six_max_speed_over_weekly_max',
 'day_minus_six_speed_departure_from_weekly_mean',
 'day_minus_six_std_speed_departure_from_weekly_mean',
 'day_minus_six_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_six_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_six_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_six_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_seven_risk_index_w',
 'day_minus_seven_risk_index',
 'day_minus_seven_relevance',
 'day_minus_seven_sum_distance',
 'day_minus_seven_min_distance',
 'day_minus_seven_max_distance',
 'day_minus_seven_mean_distance',
 'day_minus_seven_std_distance',
 'day_minus_seven_min_speed',
 'day_minus_seven_max_speed',
 'day_minus_seven_mean_speed',
 'day_minus_seven_std_speed',
 'day_minus_seven_prealert_low_count',
 'day_minus_seven_prealert_mid_count',
 'day_minus_seven_prealert_high_count',
 'day_minus_seven_alert_low_count',
 'day_minus_seven_alert_mid_count',
 'day_minus_seven_alert_high_count',
 'day_minus_seven_alert_speed_limit_low_count',
 'day_minus_seven_alert_speed_limit_mid_count',
 'day_minus_seven_alert_speed_limit_high_count',
 'day_minus_seven_no_alert_flag',
 'day_minus_seven_pre_alert_count_by_100km',
 'day_minus_seven_alert_count_by_100km',
 'day_minus_seven_speed_limit_alert_count_by_100km',
 'day_minus_seven_mixed_alert_count_by_100km',
 'day_minus_seven_no_alert_count_by_100km',
 'day_minus_seven_max_speed_over_weekly_max',
 'day_minus_seven_speed_departure_from_weekly_mean',
 'day_minus_seven_std_speed_departure_from_weekly_mean',
 'day_minus_seven_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_seven_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_seven_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_seven_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_eight_risk_index_w',
 'day_minus_eight_risk_index',
 'day_minus_eight_relevance',
 'day_minus_eight_sum_distance',
 'day_minus_eight_min_distance',
 'day_minus_eight_max_distance',
 'day_minus_eight_mean_distance',
 'day_minus_eight_std_distance',
 'day_minus_eight_min_speed',
 'day_minus_eight_max_speed',
 'day_minus_eight_mean_speed',
 'day_minus_eight_std_speed',
 'day_minus_eight_prealert_low_count',
 'day_minus_eight_prealert_mid_count',
 'day_minus_eight_prealert_high_count',
 'day_minus_eight_alert_low_count',
 'day_minus_eight_alert_mid_count',
 'day_minus_eight_alert_high_count',
 'day_minus_eight_alert_speed_limit_low_count',
 'day_minus_eight_alert_speed_limit_mid_count',
 'day_minus_eight_alert_speed_limit_high_count',
 'day_minus_eight_no_alert_flag',
 'day_minus_eight_pre_alert_count_by_100km',
 'day_minus_eight_alert_count_by_100km',
 'day_minus_eight_speed_limit_alert_count_by_100km',
 'day_minus_eight_mixed_alert_count_by_100km',
 'day_minus_eight_no_alert_count_by_100km',
 'day_minus_eight_max_speed_over_weekly_max',
 'day_minus_eight_speed_departure_from_weekly_mean',
 'day_minus_eight_std_speed_departure_from_weekly_mean',
 'day_minus_eight_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_eight_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_eight_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_eight_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_nine_risk_index_w',
 'day_minus_nine_risk_index',
 'day_minus_nine_relevance',
 'day_minus_nine_sum_distance',
 'day_minus_nine_min_distance',
 'day_minus_nine_max_distance',
 'day_minus_nine_mean_distance',
 'day_minus_nine_std_distance',
 'day_minus_nine_min_speed',
 'day_minus_nine_max_speed',
 'day_minus_nine_mean_speed',
 'day_minus_nine_std_speed',
 'day_minus_nine_prealert_low_count',
 'day_minus_nine_prealert_mid_count',
 'day_minus_nine_prealert_high_count',
 'day_minus_nine_alert_low_count',
 'day_minus_nine_alert_mid_count',
 'day_minus_nine_alert_high_count',
 'day_minus_nine_alert_speed_limit_low_count',
 'day_minus_nine_alert_speed_limit_mid_count',
 'day_minus_nine_alert_speed_limit_high_count',
 'day_minus_nine_no_alert_flag',
 'day_minus_nine_pre_alert_count_by_100km',
 'day_minus_nine_alert_count_by_100km',
 'day_minus_nine_speed_limit_alert_count_by_100km',
 'day_minus_nine_mixed_alert_count_by_100km',
 'day_minus_nine_no_alert_count_by_100km',
 'day_minus_nine_max_speed_over_weekly_max',
 'day_minus_nine_speed_departure_from_weekly_mean',
 'day_minus_nine_std_speed_departure_from_weekly_mean',
 'day_minus_nine_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_nine_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_nine_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_nine_mixed_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_ten_risk_index_w',
 'day_minus_ten_risk_index',
 'day_minus_ten_relevance',
 'day_minus_ten_sum_distance',
 'day_minus_ten_min_distance',
 'day_minus_ten_max_distance',
 'day_minus_ten_mean_distance',
 'day_minus_ten_std_distance',
 'day_minus_ten_min_speed',
 'day_minus_ten_max_speed',
 'day_minus_ten_mean_speed',
 'day_minus_ten_std_speed',
 'day_minus_ten_prealert_low_count',
 'day_minus_ten_prealert_mid_count',
 'day_minus_ten_prealert_high_count',
 'day_minus_ten_alert_low_count',
 'day_minus_ten_alert_mid_count',
 'day_minus_ten_alert_high_count',
 'day_minus_ten_alert_speed_limit_low_count',
 'day_minus_ten_alert_speed_limit_mid_count',
 'day_minus_ten_alert_speed_limit_high_count',
 'day_minus_ten_no_alert_flag',
 'day_minus_ten_pre_alert_count_by_100km',
 'day_minus_ten_alert_count_by_100km',
 'day_minus_ten_speed_limit_alert_count_by_100km',
 'day_minus_ten_mixed_alert_count_by_100km',
 'day_minus_ten_no_alert_count_by_100km',
 'day_minus_ten_max_speed_over_weekly_max',
 'day_minus_ten_speed_departure_from_weekly_mean',
 'day_minus_ten_std_speed_departure_from_weekly_mean',
 'day_minus_ten_pre_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_ten_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_ten_speed_limit_alert_count_by_100km_departure_from_from_weekly_mean',
 'day_minus_ten_mixed_alert_count_by_100km_departure_from_from_weekly_mean'
]
geofences = [
    [-22.8057070703432,-69.2734090450553],
    [-21.1341130342968,-69.5767837018216],
    [-32.8797459651116,-70.7780985185238],
    [-24.2525048005818,-69.0537217566103],
    [-23.6016808151588,-70.3750371928694],
    [-20.0633697158096,-69.2629475094755],
    [-36.8302622837311,-72.1485937259326],
    [-27.3264128822389,-70.5519650153489],
    [-22.2695866079911,-69.6351568357147],
    [-20.2642166837292,-70.1019851259824],
    [-29.8030779536697,-71.278941483055],
    [-41.4788692909064,-73.0962779176197],
    [-22.6023419458136,-69.0976014211763],
    [-20.5490206686942,-69.652414161256],
    [-23.0764573622445,-70.3718030553243],
    [-18.6345832376816,-70.2027119652586],
    [-24.3909050989714,-69.969492214819],
    [-25.6436003744412,-70.2937111210338],
    [-31.8911259614106,-71.3422837585],
    [-22.1629030987645,-70.1596966812095],
    [-23.2916648034877,-69.7193076119961],
    [-20.2500474744227,-69.7496376652675],
    [-23.9533241742318,-69.7136633549328],
    [-35.3755650492931,-71.5655112879138],
    [-28.2426636384951,-70.6045944150991],
    [-21.6158803585441,-69.5448973414707],
    [-20.8420352828159,-68.7030974248683],
    [-23.7607766096737,-70.2694979761733],
    [-26.4296746805242,-70.6040596125916],
    [-20.8028200876344,-69.6926661716191],
    [-22.9256871974335,-68.1397373293215],
    [-24.255687527893,-69.1171009571172],
    [-38.8190698772965,-72.5397048688225],
    [-20.8201988181122,-70.057709036747],
    [-31.2040827529945,-71.5575494942839],
    [-23.0064946279446,-69.0914443550757],
    [-24.1442885936388,-68.3955684214136],
    [-22.7507165168552,-69.3185655812792],
    [-22.4282350891153,-68.8836802501008],
    [-37.168545644112,-73.2008749908628],
    [-32.6850701567042,-71.3491198075849],
    [-23.4416571813597,-70.0722150422576],
    [-24.4808485956354,-65.8438884544288],
    [-19.3349828646502,-70.0032708085794],
    [-26.4883211699603,-69.72199099007],
    [-33.5738402201532,-70.62588815338],
    [-22.6446986477387,-70.263672690419],
    [-20.1673064439598,-69.5050522601248],
    [-23.8124715235815,-69.9470264158428],
    [-30.5992940782271,-71.2587817293798],
    [-29.1050640739918,-70.9556991995684],
    [-23.3593443755416,-70.3975898209279],
    [-21.9795388544678,-69.5784339368348],
    [-40.2666769470707,-73.1411931563636],
    [-23.7292834965471,-70.4359094271721],
    [-23.0407662823212,-69.5035972804431],
    [-24.1281196576539,-69.4040257295376],
    [-25.0754317492935,-69.8951993868434],
    [-22.6587882865592,-69.6489113424645],
    [-24.3586744781459,-69.0995563893276]
]

def get_patente_history(patente, n_days):
    return DetallePatenteDia.query.filter_by(patente=patente).order_by(DetallePatenteDia.date.desc()).limit(n_days).all(), 200

def get_patente_ranking_change(patente):
    return DetallePatenteDia.query.filter_by(patente=patente).order_by(DetallePatenteDia.step.desc()).limit(n_days).all(), 200

def get_component_series(patente):
    valores = DetallePatenteDia.query.filter_by(patente=patente).order_by(DetallePatenteDia.date.asc()).limit(10).all()
    mean_speed_weekly = valores[0].mean_speed / (1.00001 + valores[0].speed_departure_from_weekly_mean)
    mean_max_speed_weekly = valores[0].max_speed / (1.00001 + valores[0].max_speed_over_weekly_max)
    prealert_mean_weekly = valores[0].pre_alert_count_by_100km / (1.00001 + valores[0].pre_alert_count_by_100km_departure_from_weekly_mean)
    alert_mean_weekly = valores[0].alert_count_by_100km / (1.00001 + valores[0].alert_count_by_100km_departure_from_weekly_mean)
    series = [
        [
            {
                'name': 'Indice de Riesgo',
                'data': [round(v.risk_index_w,2) for v in valores]
            },
        ]
        ,
        [
            {
                'name': 'Distancia (Km.)',
                'data': [round(v.sum_distance,2) for v in valores]
            },
        ],
        [
            {
                'name': 'Velocidad Km/h',
                'data': [round(v.mean_speed,2) for v in valores]
            },
            {
                'name': 'Media Global',
                'data': [round(mean_speed_weekly,2)] * 10
            },
        ],
        [
            {
                'name': 'Velocidad Km/h',
                'data': [round(v.max_speed,2) for v in valores]
            },
            {
                'name': 'Media Global',
                'data': [round(mean_max_speed_weekly,2)] * 10
            },
        ],
        [
            {
                'name': 'No. Prealertas',
                'data': [round(v.pre_alert_count_by_100km,0) for v in valores]
            },
            {
                'name': 'Media Global',
                'data': [round(prealert_mean_weekly,2)] * 10
            },
        ],
        [
            {
                'name': 'No. Alertas',
                'data': [round(v.alert_count_by_100km,0) for v in valores]
            },
            {
                'name': 'Media Global',
                'data': [round(alert_mean_weekly,2)] * 10
            },
        ]
    ]
    return series, 200

def get_decision_plot(patente, step_id_week):
    f = plt.figure()
    ranker = joblib.load('C:/Users/raskolnnikov/Desktop/projects/samtech/samtech_entrega/modelos/ranker_v_1.0.joblib')
    explainer = shap.TreeExplainer(ranker)
    ranker_features = ranker.feature_names
    expected_value = explainer.expected_value
    entry = RankingEntry.query.filter_by(patente=patente, step_id_week=step_id_week).one().instance_json
    instance = pd.read_json(entry, orient='records').T
    instance.columns = ranker_features
    shap_value = ranker.predict(
        xgb.DMatrix(instance[ranker_features]),
        pred_contribs=True,
    )[0,:-1]
    shap.decision_plot(expected_value,shap_value, instance.iloc[0,:], link='logit', highlight=0, show = False)
    buf = BytesIO()
    f.savefig(buf, format = "png",
                dpi = 150,
                bbox_inches = 'tight')
    buf.seek(0)
    f.clear()
    plt.close(f)
    img_base64 = base64.b64encode(buf.read())
    response = {
         "image": img_base64.decode(),
    }
    return response,200

def get_geofences(patente, step_id_week):
    map_pickup = folium.Map( location=[-24.25340,-69.05596], zoom_start=6)
    idx = np.random.randint(0,60,30)
    for i,coord in enumerate(geofences):
        if i in idx:
            folium.Marker(location=[coord[0], coord[1]]).add_to(map_pickup)
    return map_pickup._repr_html_(), 200



def save_changes(data):
    db.session.add(data)
    db.session.commit()

import os
import pickle
import numpy as np
import pandas as pd
import artm

from glob import glob


def get_data(df):
    """
    The function implements converting DataFrame with information about MCC-codes and costs of the client
     to his profile. The profile include information about behaviour pattern, gender and age.

    :param df: pandas.DataFrame with two columns: first with MCC, second with costs on the MCC.
    :return: python dict
    """
    topic2name = pickle.load(open('../backend/data/topic2name.pkl', 'rb'))
    with open('../backend/tmp/1.vw', 'w') as f:
        f.write('0 |@default')
        for i, j in zip(df.values[:, 0], df.values[:, 1]):
            f.write(' {}:{}'.format(int(i), int(j)))
        f.write('\n')

    batch_vectorizer = artm.BatchVectorizer(target_folder='../backend/tmp',
                                            data_path='../backend/tmp/1.vw',
                                            data_format='vowpal_wabbit')

    model = artm.load_artm_model('../backend/data/reg_plsa_nogrp_mlt')
    profile = model.transform(batch_vectorizer)
    top_topics = profile.sort_values(by=profile.columns[0], ascending=False).index[:5].values
    top_topics = [topic2name[i] for i in top_topics]
    top_topics_score = profile.sort_values(by=profile.columns[0], ascending=False).values[:5].reshape(5)
    top_topics = dict(zip(top_topics, top_topics_score))
    gender = model.get_phi(class_ids=['@gender']).loc[['M', 'F']].values.dot(profile.values).reshape(2)
    age = model.get_phi(class_ids=['@age']).loc[['teen', 'young', 'midage', 'elderly']].values.dot(
        profile.values).reshape(4)

    filelist = glob('../backend/tmp/*')
    for f in filelist:
        os.remove(f)
    return {'top_topics': top_topics, 'gender': list(gender), 'age': list(age)}


def change_chart():
    """
    The function change server/pages/templates/index.html according to upload files with information about client
    :return:
    """
    df = pd.read_csv('../backend/tmp/data.csv')
    predict = get_data(df)
    with open('../backend/code/index.html', 'r') as f:
        html = f.read()

    html = html.replace('male_pobability', str(np.uint8(predict['gender'][0] * 100)))
    html = html.replace('female_probability', str(np.uint8(predict['gender'][1] * 100)))

    html = html.replace('teen_age', str(np.uint8(predict['age'][0] * 100)))
    html = html.replace('young_age', str(np.uint8(predict['age'][1] * 100)))
    html = html.replace('middle_age', str(np.uint8(predict['age'][2] * 100)))
    html = html.replace('elderly_age', str(np.uint8(predict['age'][3] * 100)))

    for i, j in enumerate(predict['top_topics'].items()):
        html = html.replace('topic_'+str(i+1), j[0])
        html = html.replace('topic_p'+str(i+1), str(np.uint8(j[1] * 100 + 1)))

    with open('./pages/templates/index.html', 'w') as f:
        f.write(html)


def init_chart():
    """
    The function initialise server/pages/templates/index.html with information about random user.
    :return:
    """
    paths = glob('../backend/data/examples/*')
    path = np.random.choice(paths)
    df = pd.read_csv(path)
    predict = get_data(df)
    with open('../backend/code/index.html', 'r') as f:
        html = f.read()

    html = html.replace('male_pobability', str(np.uint8(predict['gender'][0] * 100)))
    html = html.replace('female_probability', str(np.uint8(predict['gender'][1] * 100)))

    html = html.replace('teen_age', str(np.uint8(predict['age'][0] * 100)))
    html = html.replace('young_age', str(np.uint8(predict['age'][1] * 100)))
    html = html.replace('middle_age', str(np.uint8(predict['age'][2] * 100)))
    html = html.replace('elderly_age', str(np.uint8(predict['age'][3] * 100)))

    for i, j in enumerate(predict['top_topics'].items()):
        html = html.replace('topic_'+str(i+1), j[0])
        html = html.replace('topic_p'+str(i+1), str(np.uint8(j[1] * 100 + 1)))

    with open('./pages/templates/index.html', 'w') as f:
        f.write(html)





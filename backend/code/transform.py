import sys
import os
import pickle
import numpy as np
import pandas as pd
sys.path.append('/home/roseaysina/bigartm/python')
import artm

from glob import glob


def get_data(df):
    mcc2descr = pickle.load(open('../backend/data/mcc2descr.pkl', 'rb'))
    with open('../backend/tmp/1.vw', 'w') as f:
        f.write('0 |@default')
        for i, j in zip(df.values[:, 0], df.values[:, 1]):
            f.write(' {}:{}'.format(int(i), int(j)))
        f.write('\n')

    batch_vectorizer = artm.BatchVectorizer(target_folder='../backend/tmp',
                                            data_path='../backend/tmp/1.vw',
                                            data_format='vowpal_wabbit')

    model = artm.load_artm_model('../backend/data/reg_plsa_grp_mlt')
    profile = model.transform(batch_vectorizer)
    phi = model.get_phi(class_ids=['@default'])
    phi.index = phi.reset_index()['index'].replace(mcc2descr)
    top_topics = profile.sort_values(by=profile.columns[0], ascending=False).index[:5].values
    top_tokens = [list(phi[i].sort_values(ascending=False)[:3].index.values) for i in top_topics]
    gender = model.get_phi(class_ids=['@gender']).loc[['M', 'F']].values.dot(profile.values).reshape(2)
    age = model.get_phi(class_ids=['@age']).loc[['teen', 'young', 'midage', 'elderly']].values.dot(
        profile.values).reshape(4)

    filelist = glob('../backend/tmp/*')
    for f in filelist:
        os.remove(f)
    return {'top_tokens': top_tokens, 'gender': list(gender), 'age': list(age)}

def change_chart():
    df = pd.read_csv('../backend/tmp/data.csv')
    predict = get_data(df)
    with open('./static/media/donutchart.txt', 'w') as f:
        f.write('Male {}\n'.format(np.uint8(predict['gender'][0] * 100)))
        f.write('Female {}\n'.format(np.uint8(predict['gender'][1] * 100)))

    with open('./static/media/barchart.txt', 'w') as f:
        f.write('Teenage {}\n'.format(np.uint8(predict['age'][0] * 100)))
        f.write('Young {}\n'.format(np.uint8(predict['age'][1] * 100)))
        f.write('Middle_age {}\n'.format(np.uint8(predict['age'][2] * 100)))
        f.write('Elderly_age {}\n'.format(np.uint8(predict['age'][3] * 100)))




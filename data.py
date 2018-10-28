# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import numpy as np
import torch
import nltk


def get_batch(batch, word_vec):
    # sent in batch in decreasing order of lengths (bsize, max_len, word_dim)
    lengths = np.array([len(x) for x in batch])
    max_len = np.max(lengths)
    embed = np.zeros((max_len, len(batch), 300))

    for i in range(len(batch)):
        for j in range(len(batch[i])):
            embed[j, i, :] = word_vec[batch[i][j]]

    return torch.from_numpy(embed).float(), lengths


def get_word_dict(sentences):
	 # create vocab of words
	f = open('word_dict.txt','w')
	word_dict = {}
	for sent in sentences:
		for word in sent.split():
			if word not in word_dict:
				word_dict[word] = ''
				f.write(word+'\n')
	word_dict['<s>'] = ''
	word_dict['</s>'] = ''
	word_dict['<p>'] = ''
	f.write('<s>'+'\n')
	f.write('</s>'+'\n')
	f.write('<p>'+'\n')
	print('Done vocab')
	return word_dict


def get_glove(word_dict, glove_path):
    # create word_vec with glove vectors
	word_vec = {}
	all_word = {}
	with open('../embedding.txt','r') as f:
		for line in f:
			if len(line.split('\t'))<2:
				continue
			word, vec = line.strip().split('\t')[0],line.strip().split('\t')[1]
			#vec = vec.replace('[','')
			#vec = vec.replace(']','')
			#vec = [float(x) for x in vec.split()]
			#print(len(vec.split()))
			if word in word_dict:
				if len(np.array(list(map(float, vec.split()))))==300:
					word_vec[word] = np.array(list(map(float, vec.split())))
				else:
					print('now' , len(np.array(list(map(float, vec.split())))))
			#all_word[word] = np.array(list(map(float, vec.split())))
	#for word in word_dict:
	#	if word not in word_vec and word.lower() not in word_vec and word.lower() in all_word:
	#		word_vec[word] = all_word[word.lower()]
	#	if word[-1]=='.' and word[:-1] not in word_vec and word[:-1] in all_word:
	#		word_vec[word] = all_word[word[:-1]]
	print('Found {0}(/{1}) words with glove vectors'.format(len(word_vec), len(word_dict)))
	return word_vec


def build_vocab(sentences, glove_path):
	word_dict = get_word_dict(sentences)
#	print(word_dict)
	word_vec = get_glove(word_dict, glove_path)
	print('Vocab size : {0}'.format(len(word_vec)))
	return word_vec


def get_nli(data_path):
    s1 = {}
    s2 = {}
    target = {}

    dico_label = {'entailment': 0, 'neutral':1 , 'contradiction':2}
#{'false': 0,  'true':1,'pants-fire':2,'half-true':3,'mostly-true':4,'barely-true':5}

    for data_type in ['train', 'dev', 'test']:
        s1[data_type], s2[data_type], target[data_type] = {}, {}, {}
        s1[data_type]['path'] = os.path.join(data_path, 's1.' + data_type)
        s2[data_type]['path'] = os.path.join(data_path, 's2.' + data_type)
        target[data_type]['path'] = os.path.join(data_path,
                                                 'labels.' + data_type)

        s1[data_type]['sent'] = [line.rstrip() for line in
                                 open(s1[data_type]['path'], 'r')]
        s2[data_type]['sent'] = [line.rstrip() for line in
                                 open(s2[data_type]['path'], 'r')]
        target[data_type]['data'] = np.array([dico_label[line.rstrip('\n')]
                for line in open(target[data_type]['path'], 'r')])

        assert len(s1[data_type]['sent']) == len(s2[data_type]['sent']) == \
            len(target[data_type]['data'])

        print('** {0} DATA : Found {1} pairs of {2} sentences.'.format(
                data_type.upper(), len(s1[data_type]['sent']), data_type))

    train = {'s1': s1['train']['sent'], 's2': s2['train']['sent'],
             'label': target['train']['data']}
    dev = {'s1': s1['dev']['sent'], 's2': s2['dev']['sent'],
           'label': target['dev']['data']}
    test = {'s1': s1['test']['sent'], 's2': s2['test']['sent'],
            'label': target['test']['data']}
    return train, dev, test

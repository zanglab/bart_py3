# Time-stamp: <2017-08-10>
'''Module for calculating ROC-AUC values for all TF datasets

Copyright (c) 2017, 2018 Chongzhi Zang, Zhenjia Wang <zhenjia@virginia.edu>

This code is free software; you can redistribute it and/or modify it 
under the terms of the BSD License.

@status: release candidate
@version: $Id$
@author: Chongzhi Zang, Zhenjia Wang
@contact: zhenjia@virginia.edu

'''

import os,sys,os.path
import argparse,time
import configparser
import re
import multiprocessing
from BART.StatTest import stat_test
from BART.OptValidator import opt_validate,conf_validate
from BART.ReadCount import read_count_on_DHS
import bz2

def get_file(filedir,match):
    mark = re.compile(match)
    names = os.listdir(filedir)
    files = []
    for name in names:
        if mark.search(name):
            files.append('_'.join(name.split('_')[:-2]))
    files = sorted(files)
    return files


def get_position_list(margefile):
    '''
    Get the ID list of DHS, according to the decreasingly sorted scores in MARGE 
    ''' 
    fin = open(margefile,'rb')
    line = fin.readline()  
    score = {}
    while line:
        line = line.strip().split()
        try:
            score[line[-2]]=float(line[-1])
        except:
            pass
        line = fin.readline()
    fin.close()
    return sorted(score.keys(),key=score.get,reverse=True)


def get_match_list(tf, tfdir,positions):
    '''
    Return the binding info on DHS
    '''   
    ## .txt format
#     fname = tf+'_DHS_01.txt'
#     tf = open(os.path.join(tfdir,fname), 'rb') 
#     lines = tf.raw.read()
    ## .bz2 format
    fname = tf+'_DHS_01.txt.bz2'
    tf = bz2.open(os.path.join(tfdir,fname),'r')
    lines = tf.read()
    match = [lines[2*position-2]-ord('0') for position in positions]
    tf.close()
    return match


def partion(match): 
 
    sub_t = 0
    list_t = []
    list_f = []
    total = len(match)  
    groupsize=10000  
    groups = int(total/groupsize)
    for i in range(groups):
        sub_t = sum(match[i*groupsize:(i+1)*groupsize])
        sub_f = groupsize - sub_t
        list_t.append(sub_t) 
        list_f.append(sub_f)

    sub_t = sum(match[groups*groupsize:])
    sub_f = total -groups*groupsize-sub_t
    list_t.append(sub_t) 
    list_f.append(sub_f)   
 
    return total, list_t, list_f
    

  
def roc_auc(total, list_t, list_f): 
    
    list_x = [0.0]
    list_y = [0.0]
    assert len(list_t)==len(list_f)
    for i in range(len(list_t)):
        list_x.append(list_f[i]+list_x[i])
        list_y.append(list_t[i]+list_y[i])
    total_t = list_y[-1]
    list_x = [i/(total - total_t) for i in list_x]
    list_y = [i/total_t for i in list_y]
    
    auc = 0.0
    for i in range(1,len(list_x)):
        width = list_x[i]-list_x[i-1]
        height = (list_y[i]+list_y[i-1])/2
        auc += height*width

    return list_x, list_y, auc

def cal_auc_for_tf(tf_p):
    tf,tfdir,positions = tf_p
#    time1 = time.time()    
    match = get_match_list(tf,tfdir,positions)
    (t, lt, lf) = partion(match)
    (list_x, list_y, auc) = roc_auc(t, lt,lf)
#    time2 = time.time()
#    print(time2-time1)
    return tf,auc

def run(options):

    args = opt_validate(options)
    tfs = get_file(args.tfdir,'DHS_01')
    
    if len(tfs) == 0:
        sys.stderr.write('Please specify correct directory of TF binding profiles!') 
        sys.exit(1)   
    try:
        os.makedirs(args.outdir,exist_ok=True)
    except:
        sys.exit('Output directory: {} could not be created.'.format(args.outdir))

    # This part is for the auc.txt input
    #if args.auc:
    #    AUCs = {}
    #    with open(args.infile,'r') as auc_infile:
    #        for auc_line in auc_infile.readlines():
    #            auc_info = auc_line.strip().split()
    #            AUCs[auc_info[0]] = float(auc_info[-1])
    #    #print(AUCs)
    #    stat_test(AUCs,args)
    #    exit(0)
    # print(args,'\n') 
    
    if args.subcommand_name == 'geneset':
        print('Prediction starts...\n\nRank all DHS...\n')
        margefile = args.infile    
        positions = get_position_list(args.infile)   
        positions = [int(i) for i in positions]
        #print(type(positions[1]));exit(0)
    elif args.subcommand_name == 'profile':
        print('Start mapping the {} file...\n'.format(args.format.upper()))
        counting = read_count_on_DHS(args)      
        positions = sorted(counting.keys(),key=counting.get,reverse=True)
        positions = [int(i) for i in positions]
        #print([[i,counting[i]] for i in positions[:30]])
        print('Prediction starts...\n\nRank all DHS...\n')

    if len(positions) == 0:
        sys.stderr.write('Input file might not with right format!\n')
        sys.exit(1)

    # output file of AUC-ROC values for all TFs    
    aucfile = args.outdir+os.sep+args.ofilename+'_auc.txt'
    
    sys.stdout.write("Calculating ROC-AUC values for all transcription factors:\n\n")
    print(args)

    tf_ps = [(tf,args.tfdir,positions) for tf in tfs]
    print(len(tf_ps),'#TF datasets')###########
    AUCs = {}
    # always multiprocessing
    if args.processes:  
        print('--Number of CUPs in use: {}\n'.format(args.processes))       
        pool = multiprocessing.Pool(processes=args.processes)
        tf_aucs = pool.map_async(cal_auc_for_tf,tf_ps,chunksize=1)
        total=len(tf_ps)  
        #print(total)
        
        #import tqdm  ##pbar
        #pbar = tqdm.tqdm(total=total) ##pbar
        #last=total ##pbar
         
        while not tf_aucs.ready(): # print percentage of work has been done
            remaining=tf_aucs._number_left            
            #pbar.update(last-remaining) ##pbar
            #last=remaining ##pbar            
            sys.stdout.write('\n  Processing...{:.1f}% finished'.format(100*(total-remaining)/total)) ##print
            i=0
            while not tf_aucs.ready() and i<24:
                sys.stdout.write('.')
                sys.stdout.flush()
                #print(".",end='',flush=True) for py3
                i+=1
                time.sleep(5)
        
        #pbar.update(remaining) ##pbar
        #pbar.close() ##pbar        
        print('\n  Processing...100.0% finished.') ##print
        pool.close()
        pool.join()
        
        # save the AUCs
        for tfauc in tf_aucs.get():
            AUCs[tfauc[0]]=tfauc[1]
        #print(AUCs)

    else:         
        for tf_p in tf_ps:
            AUCs[tf_p[0]]=cal_auc_for_tf(tf_p)[1]

    with open(aucfile, 'w') as aucf:
        for tf_key in sorted(AUCs.keys(),key=AUCs.get,reverse=True):
            aucf.write('{}\tAUC = {:.3f}\n'.format(tf_key,AUCs[tf_key]))
    print('\n--ROC-AUC calculation finished!\n--Results saved in file: {}\n'.format(aucfile))
    stat_test(AUCs,args)


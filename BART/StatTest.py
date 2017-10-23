# Time-stamp: <2017-08-10>
'''Module for calculating the Wilcoxon-score and p value for each unique TF 

Copyright (c) 2017, 2018 Chongzhi Zang, Zhenjia Wang <zhenjia@virginia.edu>

This code is free software; you can redistribute it and/or modify it 
under the terms of the BSD License.

@status: release candidate
@version: $Id$
@author: Chongzhi Zang, Zhenjia Wang
@contact: zhenjia@virginia.edu

'''
import argparse,os,sys,re

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from BART.OptValidator import opt_validate,conf_validate

def stat_plot(stat,tfs,ID,args,col):
    # box-plot
    fig=plt.figure(figsize=(4,4))
    if not args.nonorm:
        #print('****')
        plt.boxplot([stat.loc[i][col] for i in stat.index])
        plt.scatter(1,stat.loc[ID][col],c='r',marker='o',s=60)
    else:
        plt.boxplot([stat.loc[i]['score'] for i in stat.index])
        plt.scatter(1,stat.loc[ID]['score'],c='r',marker='o',s=60)
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.title(ID,fontsize = 12)
    plt.ylabel('Rank Score',fontsize = 12)
    plotdir = args.outdir+os.sep+'{}_plot'.format(args.ofilename)
    #os.makedirs(plotdir,exist_ok=True)
    try:
        os.makedirs(plotdir,exist_ok=True)
    except:
        sys.exit('Output directory: {} could not be created.'.format(plotdir))
    figname1 = plotdir+os.sep+'{}_avg_z_p_boxplot'.format(ID)
    plt.savefig(figname1,bbox_inches='tight')
    plt.close()    
    
    
    #Cumulative Fraction plot
    background = []
    for tf in tfs:
        background.extend(tfs[tf])
    target = tfs[ID]       
    background = sorted(background)
    fig=plt.figure(figsize=(4,4))   
    dx = 0.01
    x = np.arange(0,1,dx)       
    by,ty = [],[]      
    for xi in x:
        by.append(sum(i< xi for i in background )/len(background))
        ty.append(sum(i< xi for i in target )/len(target))
    plt.plot(x,by,'b-',label='ALL') 
    plt.plot(x,ty,'r-',label='{}'.format(ID)) 
    plt.legend()
    #maxval = max(background)
    #minval = min(background)
    #plt.ylim([0,1])
    #plt.xlim([0,1])
    plt.ylabel('Cumulative Fraction',fontsize=12)
    plt.xlabel('AUC',fontsize=12)
    figname2 = plotdir+os.sep+'{}_cumulative_distribution'.format(ID)
    plt.savefig(figname2,bbox_inches='tight')
    plt.close()


def stat_test(AUCs,args): 
    # read AUCs according to TF type
    print('Statistical tests start.\n')
    tfs = {}
    sam1 = []
    for tf_key in AUCs.keys():
        tf = tf_key.split('_')[0]
        auc = AUCs[tf_key]
        sam1.append(auc)
        if tf not in tfs:
            tfs[tf] = [auc]
        else:
            tfs[tf].append(auc)
    
    cols = ['score','pvalue','max_auc','zscore','rank_score','rank_zscore','rank_pvalue','rank_auc','rank_avg_z_p','rank_avg_z_p_a']
    stat = pd.DataFrame(index = [tf for tf in tfs],columns = cols)
    #stat = {}
    for tf in tfs.keys():
        if len(tfs[tf])>0: # filter the tf with few samples
            #stat_test = stats.mstats.ks_twosamp(sam1,tfs[tf],alternative='greater')
            stat_test = stats.ranksums(tfs[tf],sam1)
            #stat[tf] = [stat_test[0],stat_test[1]]
            stat.loc[tf]['score'] = stat_test[0]
            stat.loc[tf]['pvalue'] = stat_test[1]  
      
    tf_stats = pd.read_csv(args.normfile,sep='\t',index_col=0)
    # cal the normalized stat-score 
    #print('Do Normalization...')
    for i in stat.index:
        #stat[i].append((stat[i][0]-tf_stats.loc[i,'mean'])/tf_stats.loc[i,'std']) #[2] for Z-Score
        stat.loc[i]['zscore'] = (stat.loc[i]['score']-tf_stats.loc[i,'mean'])/tf_stats.loc[i,'std']
        stat.loc[i]['max_auc'] = max(tfs[i])
    
    
    # rank the list by the average rank of stat-score and z-score
    # rank of Wilcoxon Socre
    rs = 1
    for i in sorted(stat.index,key = lambda x: stat.loc[x]['score'],reverse=True): 
        #print(i,stat[i])
        stat.loc[i]['rank_score'] = rs #  rank of stat_score
        #print(i,stat[i],'\n')
        rs +=1
    
    # rank of Z-Score
    rz = 1
    for i in sorted(stat.index,key = lambda x: stat.loc[x]['zscore'],reverse=True):        
        stat.loc[i]['rank_zscore'] = rz # rank of z-score
        #print(i,stat[i])
        rz +=1 
               
    # rank of pvalue
    rp = 1
    for i in sorted(stat.index,key = lambda x: stat.loc[x]['pvalue'],reverse=False):        
        stat.loc[i]['rank_pvalue'] = rp #  rank of pvalue
        #print(i,stat[i])
        rp +=1

    ra = 1
    for i in sorted(stat.index,key = lambda x: stat.loc[x]['max_auc'],reverse=True):        
        stat.loc[i]['rank_auc'] = ra #  rank of pvalue
        #print(i,stat[i])
        ra +=1
                
    # rank of average
    for i in stat.index:
        stat.loc[i]['rank_avg_z_p'] = (stat.loc[i]['rank_zscore']+stat.loc[i]['rank_pvalue'])*0.5   # [6] for average of stat-score and z-score
        stat.loc[i]['rank_avg_z_p_a'] = (stat.loc[i]['rank_zscore']+stat.loc[i]['rank_pvalue']+stat.loc[i]['rank_auc'])*0.33   # [7] for average of three

        #print(i,stat[i]) 



    statfile = args.outdir+os.sep+args.ofilename+'_bart_results.txt'
    with open(statfile,'w') as statout:
        statout.write('TF\t{}\t{}\t{}\t{}\t{}\n'.format('statistic','pvalue','zscore','max_auc','rela_rank'))
        for i in sorted(stat.index,key=lambda x: stat.loc[x]['rank_avg_z_p_a'],reverse=False):
            statout.write('{}\t{:.3f}\t{:.3e}\t{:.3f}\t{:.3f}\t{:.3f}\n'.format(i,stat.loc[i]['score'],stat.loc[i]['pvalue'],stat.loc[i]['zscore'],stat.loc[i]['max_auc'],stat.loc[i]['rank_avg_z_p_a']/len(tfs.keys())))
    print('--Standardization finished!\n--Ranked TFs saved in file: {}\n'.format(statfile))
    
    # plot figures of user defined TFs
    if args.target:
        with open(args.target) as target_file:
            IDs = [re.split('[^a-zA-Z0-9]+',line)[0] for line in target_file.readlines()]
            for ID in IDs:
                stat_plot(stat,tfs,ID,args,'rank_avg_z_p_a')
        
    print('Prediction done!\n')

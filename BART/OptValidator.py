# Time-stamp: <2017-08-10>
'''
Copyright (c) 2017, 2018 Chongzhi Zang, Zhenjia Wang <zhenjia@virginia.edu>

This code is free software; you can redistribute it and/or modify it 
under the terms of the BSD License.

@status: release candidate
@version: $Id$
@author: Chongzhi Zang, Zhenjia Wang
@contact: zhenjia@virginia.edu

'''

import configparser
import os,re,sys


def conf_validate():

    # read user provided path from config file
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),'bart.conf'))

    return  config


def opt_validate(options):
    
    config = conf_validate()
    
    if not options.outdir:
        options.outdir = os.getcwd()+os.sep+'bart_output'
        #chroms = hg_chrom

    if not options.ofilename:
        #infilebase = os.path.basename(options.infile).split('.txt')[0] 
        infilebase = re.split('.txt|.bed|.bam',os.path.basename(options.infile))[0] 
        if "_".join(infilebase.split('_')[-2:]) == "enhancer_prediction":
            options.ofilename = "_".join(infilebase.split('_')[:-2])
        else :
            options.ofilename = infilebase
        #options.ofilename = os.path.basename(options.infile).split('.')[0] 
    
    # config the dir of data, separate by species
    if options.species == 'hg38':   
        if config['path']['hg38_library_dir']:
            data_dir = config['path']['hg38_library_dir']+os.sep+'hg38_library' 
        else:
            sys.stderr.write('ERROR!! The path to the data library need to be specified!\n') 
            sys.stderr.write('Please revise the <bart.conf> file before installation!\n\n') 
            sys.exit(1)  
            #data_dir = os.path.dirname(__file__)+os.sep+'hg38_library'
        
        #used for local test
        try:
            options.tfdir = config['path']['hg38_data_tf_dir']  
        except:
            options.tfdir = data_dir+os.sep+'hg38_TF_binding'  
        
        if options.subcommand_name == 'geneset':
            options.normfile = data_dir+os.sep+'hg38_MSigDB.dat'           
        elif options.subcommand_name=='profile':
            options.normfile = data_dir+os.sep+'hg38_H3K27ac.dat'   
            options.dhsfile = data_dir+os.sep+'hg38_UDHS.bed'
            
            
    elif options.species == 'mm10': 
        if config['path']['mm10_library_dir']:
            data_dir = config['path']['mm10_library_dir']+os.sep+'mm10_library' 
        else:
            sys.stderr.write('ERROR!! The path to the data library need to be specified!\n') 
            sys.stderr.write('Please revise the <bart.conf> file before installation!\n\n') 
            sys.exit(1)  
            #data_dir = os.path.dirname(__file__)+os.sep+'mm10_library'
            
        # used for local test
        try:
            options.tfdir = config['path']['mm10_data_tf_dir']  
        except:
            options.tfdir = data_dir+os.sep+'mm10_TF_binding'        
        
        if options.subcommand_name == 'geneset':
            options.normfile = data_dir+os.sep+'mm10_H3K27ac.dat'           
        elif options.subcommand_name=='profile':
            options.normfile = data_dir+os.sep+'mm10_H3K27ac.dat'   
            options.dhsfile = data_dir+os.sep+'mm10_UDHS.bed'      

    return options
    

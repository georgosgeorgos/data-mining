#!/bin/bash

printf "Start!\n"

mkdir output
cd output
mkdir defaultStemmer
mkdir englishStemmer
mkdir englishStopwords
cd ..
sleep 1s

printf "\n nMDCG \n"

python evaluation_nMDCG.py ./output/defaultStemmer/output_cran_defaultStemmer_count.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "defaultStemmer_count"
python evaluation_nMDCG.py ./output/defaultStemmer/output_cran_defaultStemmer_tfidf.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "defaultStemmer_tfidf"
python evaluation_nMDCG.py ./output/defaultStemmer/output_cran_defaultStemmer_bm25.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv   "defaultStemmer_bm25"

python evaluation_nMDCG.py ./output/englishStemmer/output_cran_englishStemmer_count.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStemmer_count"
python evaluation_nMDCG.py ./output/englishStemmer/output_cran_englishStemmer_tfidf.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStemmer_tfidf"
python evaluation_nMDCG.py ./output/englishStemmer/output_cran_englishStemmer_bm25.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStemmer_bm25"

python evaluation_nMDCG.py ./output/englishStopwords/output_cran_englishStopwords_count.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_count"
python evaluation_nMDCG.py ./output/englishStopwords/output_cran_englishStopwords_tfidf.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_tfidf"
python evaluation_nMDCG.py ./output/englishStopwords/output_cran_englishStopwords_bm25.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_bm25"


printf "\n R \n"
sleep 2s



python evaluation_R.py ./output/defaultStemmer/output_cran_defaultStemmer_count.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "defaultStemmer_count"
python evaluation_R.py ./output/defaultStemmer/output_cran_defaultStemmer_tfidf.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "defaultStemmer_tfidf"
python evaluation_R.py ./output/defaultStemmer/output_cran_defaultStemmer_bm25.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv   "defaultStemmer_bm25"

python evaluation_R.py ./output/englishStemmer/output_cran_englishStemmer_count.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStemmer_count"
python evaluation_R.py ./output/englishStemmer/output_cran_englishStemmer_tfidf.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStemmer_tfidf"
python evaluation_R.py ./output/englishStemmer/output_cran_englishStemmer_bm25.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStemmer_bm25"

python evaluation_R.py ./output/englishStopwords/output_cran_englishStopwords_count.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_count"
python evaluation_R.py ./output/englishStopwords/output_cran_englishStopwords_tfidf.tsv ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_tfidf"
python evaluation_R.py ./output/englishStopwords/output_cran_englishStopwords_bm25.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_bm25"





printf "\n fagin \n"
sleep 1s

python fagin.py ./output/output_cran_englishStopwords_bm25_title.tsv  ./output/output_cran_englishStopwords_bm25_text.tsv ./output/output_cran_englishStopwords_bm25_text_title.tsv 20


#java Fagin ./output/output_cran_englishStopwords_bm25_title.tsv  ./output/output_cran_englishStopwords_bm25_text.tsv ./output/output_cran_englishStopwords_bm25_text_title_java.tsv 20


printf "\n"
python evaluation_nMDCG.py ./output/output_cran_englishStopwords_bm25_title.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_bm25_title"
python evaluation_nMDCG.py ./output/output_cran_englishStopwords_bm25_text.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_bm25_text"
python evaluation_nMDCG.py ./output/output_cran_englishStopwords_bm25_text_title.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_bm25_title_text"

python evaluation_R.py ./output/output_cran_englishStopwords_bm25_title.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_bm25_title"
python evaluation_R.py ./output/output_cran_englishStopwords_bm25_text.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_bm25_text"
python evaluation_R.py ./output/output_cran_englishStopwords_bm25_text_title.tsv  ./Cranfield_DATASET/Cranfield_DATASET/cran_Ground_Truth.tsv  "englishStopwords_bm25_title_text"



printf "\n All Done :)"
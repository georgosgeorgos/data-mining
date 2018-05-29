#!/bin/bash

printf "Start!\n"
sleep 1s

mkdir output
cd output
mkdir defaultStemmer
mkdir englishStemmer
mkdir englishStopwords
cd ..


printf "\n create collections \n"
sleep 1s
#1 Create a collection on the set of html documents with MG4J.

find ./Cranfield_DATASET/Cranfield_DATASET/cran -iname \*.html | java it.unimi.di.big.mg4j.document.FileSetDocumentCollection -f HtmlDocumentFactory -p encoding=UTF-8 cran_defaultStemmer.collection

find ./Cranfield_DATASET/Cranfield_DATASET/cran -iname \*.html | java it.unimi.di.big.mg4j.document.FileSetDocumentCollection -f HtmlDocumentFactory -p encoding=UTF-8 cran_englishStemmer.collection

find ./Cranfield_DATASET/Cranfield_DATASET/cran -iname \*.html | java it.unimi.di.big.mg4j.document.FileSetDocumentCollection -f HtmlDocumentFactory -p encoding=UTF-8 cran_englishStopwords.collection


#2 Create an inverted index (with MG4J) on the collection trying different stemming methods:

#a. default stemmer,
#b. English stemmer ​ and
#c. English stemmer able to filter stopwords.


printf "\n create inverted indices \n"
sleep 1s

java it.unimi.di.big.mg4j.tool.IndexBuilder --downcase -S cran_defaultStemmer.collection cran_defaultStemmer

java it.unimi.di.big.mg4j.tool.IndexBuilder -t it.unimi.di.big.mg4j.index.snowball.EnglishStemmer -S cran_englishStemmer.collection cran_englishStemmer

java it.unimi.di.big.mg4j.tool.IndexBuilder -t homework.EnglishStemmerStopwords -S cran_englishStopwords.collection cran_englishStopwords

#3 Obtain results for each query using the software "​ homework.RunAllQueries_HW​ " trying different scorer functions: CountScorer, ​TfIdfScorer ​and BM25Scorer.


printf "\n run queries on cran_defaultStemmer \n"
sleep 1s

#cran1
java homework.RunAllQueries_HW "cran_defaultStemmer" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "CountScorer" "text_and_title" ./output/defaultStemmer/output_cran_defaultStemmer_count.tsv

java homework.RunAllQueries_HW "cran_defaultStemmer" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "TfIdfScorer" "text_and_title" ./output/defaultStemmer/output_cran_defaultStemmer_tfidf.tsv

java homework.RunAllQueries_HW "cran_defaultStemmer" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "BM25Scorer" "text_and_title" ./output/defaultStemmer/output_cran_defaultStemmer_bm25.tsv

printf "\n run queries on cran_englishStemmer \n"
sleep 1s

#cran2
java homework.RunAllQueries_HW "cran_englishStemmer" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "CountScorer" "text_and_title" ./output/englishStemmer/output_cran_englishStemmer_count.tsv

java homework.RunAllQueries_HW "cran_englishStemmer" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "TfIdfScorer" "text_and_title" ./output/englishStemmer/output_cran_englishStemmer_tfidf.tsv

java homework.RunAllQueries_HW "cran_englishStemmer" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "BM25Scorer" "text_and_title" ./output/englishStemmer/output_cran_englishStemmer_bm25.tsv

printf "\n run queries on cran_englishStopwords \n"
sleep 1s

#cran3
java homework.RunAllQueries_HW "cran_englishStopwords" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "CountScorer" "text_and_title" ./output/englishStopwords/output_cran_englishStopwords_count.tsv

java homework.RunAllQueries_HW "cran_englishStopwords" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "TfIdfScorer" "text_and_title" ./output/englishStopwords/output_cran_englishStopwords_tfidf.tsv

java homework.RunAllQueries_HW "cran_englishStopwords" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "BM25Scorer" "text_and_title" ./output/englishStopwords/output_cran_englishStopwords_bm25.tsv





printf "\n run queries on cran_englishStopwords BM25Scorer for title \n"
sleep 1s

java homework.RunAllQueries_HW "cran_englishStopwords" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "BM25Scorer" "title" ./output/output_cran_englishStopwords_bm25_title.tsv


printf "\n run queries on cran_englishStopwords BM25Scorer for text \n"
sleep 1s

java homework.RunAllQueries_HW "cran_englishStopwords" ./Cranfield_DATASET/Cranfield_DATASET/cran_all_queries.tsv "BM25Scorer" "text" ./output/output_cran_englishStopwords_bm25_text.tsv


printf "All Done :)"





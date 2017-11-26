s <- suppressPackageStartupMessages
s(require(ggplot2))
s(require(data.table))
s(require(ggthemes))
s(require(readtext))
s(require(quanteda))
s(require(topicmodels))
s(require(LDAvis))

##################### TF-IDF Filtering Functions ############ #############

PrintTermTFIDF <- function(dfm_quanteda){
  # Method was replicated from topicmodels publication on the Journal of Statistical Software by Grun and Hornik, 2011.
  #This function prints the terms tf-idf values in quartiles. The rule of thumb used in the journal is to use the value immediately before the mean when deciding the filtering threshold for FilterDFMByTFIDF.
  dfm_tm <- convert(dfm_quanteda,to="tm")
  #print(summary(col_sums(dfm_tm)))
  term_tfidf <- tapply(dfm_tm$v/row_sums(dfm_tm)[dfm_tm$i], dfm_tm$j, mean) * log2(nrow(dfm_tm)/col_sums(dfm_tm > 0))
  print(summary(term_tfidf))
}

PlotTermTFIDF <- function(dfm_quanteda,filter.by.term=FALSE,n.terms.threshold=5000){
  # Method was replicated from topicmodels publication on the Journal of Statistical Software by Grun and Hornik, 2011.
  #This function prints the terms tf-idf values in quartiles. The rule of thumb used in the journal is to use the value immediately before the mean when deciding the filtering threshold for FilterDFMByTFIDF.
  dfm_tm <- convert(dfm_quanteda,to="tm")
  #print(summary(col_sums(dfm_tm)))
  term_tfidf <- tapply(dfm_tm$v/row_sums(dfm_tm)[dfm_tm$i], dfm_tm$j, mean) * log2(nrow(dfm_tm)/col_sums(dfm_tm > 0))
  
  term.tfidf.sort <- sort(term_tfidf,decreasing = TRUE)
  
  
  plot.table <- data.table(n.terms=1:length(term.tfidf.sort),tfidf=term.tfidf.sort)
  if(filter.by.term==TRUE) plot.table <- plot.table[n.terms < n.terms.threshold]
  p <- ggplot(data=plot.table, aes(x=tfidf, y=n.terms)) + geom_line() + theme_minimal()
  return(p)
}

ListTermTFIDF <- function(dfm_quanteda){
  # Method was replicated from topicmodels publication on the Journal of Statistical Software by Grun and Hornik, 2011.
  #This function prints the terms tf-idf values in quartiles. The rule of thumb used in the journal is to use the value immediately before the mean when deciding the filtering threshold for FilterDFMByTFIDF.
  dfm_tm <- convert(dfm_quanteda,to="tm")
  #print(summary(col_sums(dfm_tm)))
  term_tfidf <- tapply(dfm_tm$v/row_sums(dfm_tm)[dfm_tm$i], dfm_tm$j, mean) * log2(nrow(dfm_tm)/col_sums(dfm_tm > 0))
  
  term.tfidf.order <- order(term_tfidf,decreasing = TRUE)
  top.terms <- dfm_tm$dimnames$Terms[term.tfidf.order]
  top.terms.score <- term_tfidf[term.tfidf.order]
  top.terms <- data.table(term=top.terms,tfidf=top.terms.score)
  
  return(top.terms)
}


FilterDFMByTFIDF <- function(dfm_quanteda,threshold){
  # The output is a dfm as defined by (tm) package. TODO: Figure out how to do it on quanteda. 
  # Method was replicated from topicmodels publication on the Journal of Statistical Software by Grun and Hornik, 2011.
  dfm_tm <- convert(dfm_quanteda,to="tm")
  term_tfidf <- tapply(dfm_tm$v/row_sums(dfm_tm)[dfm_tm$i], dfm_tm$j, mean) * log2(nrow(dfm_tm)/col_sums(dfm_tm > 0))
  dfm_tm <- dfm_tm[, term_tfidf >= threshold]
  dfm_tm <- dfm_tm[row_sums(dfm_tm) > 0,]
  return(dfm_tm)
}


############# LDA Model Fitting Functions ##################

CalculateLDAModelsUpToN <-function(dfm,N){
  #Returns a list, where every position is a created model. List starts on k=2. 
  if(class(dfm)[1] == "dfmSparse"){ #Quanteda package, needs conversion to topicmodels
    dfm <- convert(dfm, to = "topicmodels")
  } 
  lda.vem <- list()
  for(i in 1:(N-1)){
    print(paste0("Creating a model for k=",i+1," topics...",sep=" "))
    lda.vem[[i]] <- LDA(dfm, k = i+1)
  }
  return(lda.vem)
}

CalculateLDAModelsInKSet <-function(dfm,Ks,method="VEM"){
  #Returns a list, where every position is a created model. List of k values must be provided as a vector. 
  if(class(dfm)[1] == "dfmSparse"){ #Quanteda package, needs conversion to topicmodels
    dfm <- convert(dfm, to = "topicmodels")
  } 
  lda.vem <- list()
  Ks.size <- length(Ks)
  for(i in 1:Ks.size){
    print(paste0("Creating a model for k=",Ks[i]," topics...",sep=" "))
    lda.vem[[i]] <- LDA(dfm, k = Ks[i],method=method)
  }
  return(lda.vem)
}


############ Making sense of Topics Functions ################

GetDocumentsPerTopicCount <- function(lda.model){
  # Returns a named numeric vector, where the names are the topics represented by a single word, and the values are the number of documents the given topic was assigned.
  topic.document.distribution <- summary(as.factor(topics(lda.model)))  
  #names(topic.document.distribution) <- get_terms(lda.model)
  return(topic.document.distribution)
}

PrintTopicsTopTerm <- function(lda.model.list){
  # Calls GetDocumentsPerTopicCount for every topic. Best used just after creating the LDA models to get a sense of them for every value of k. 
  # WARNING: This can be HIGHLY misleading since a topic is a distribution and the top term may have a very close probability to occur as other term. 
  for(i in 1:length(lda.model.list)){
    topic.document.counts[[i]] <- GetDocumentsPerTopicCount(lda.model.list[[i]])
    cat("LDA k=",lda.model.list[[i]]@k,"\n")
    print(topic.document.counts[[i]])
    cat("\n")
  }  
}

GetDocumentsOfTopTopicK <- function(lda.model,k){
  # Returns a vector of characters, where each element is the name of a document associated to topic K. 
  # WARNING: This can be HIGHLY misleading since a document have a distribution over topics and the top topic may have a very close probability to occur as the other topic.
  return(names(topics(lda.model)[topics(lda.model) == k]))
}


GetTopicTermMatrices <- function(lda.model.list,n.terms=10){
  terms.and.topics <- lapply(lda.model.list,posterior)  
  topic.term.matrices <- lapply(terms.and.topics,"[[","terms")
  #topic <- topic.matrix[i,]
  #ordered.positions.topic <- order(-topic)
  #table <- data.table(terms=topic.model@terms[ordered.positions.topic],score=topic[ordered.positions.topic])
  ordered.topic.term.matrices <- lapply(topic.term.matrices,AuxiliaryOrderTopicTermMatrices,n.terms)
  return(ordered.topic.term.matrices)
}
AuxiliaryOrderTopicTermMatrices <- function(topic.term.matrix,n.terms){
  # This auxiliary function for GetDocumentTopicMatrices turns a DocumentTermMatrix from LDA into a list of ordered numeric vectors and a list of ordered topic names.
  topic.term.list <- apply(topic.term.matrix, 1, as.list)
  topic.term.list <- lapply(topic.term.list,as.numeric) #turn every document of the list into a numeric vector so ordering can be performed
  topic.top.topics <- lapply(topic.term.list,order,decreasing=TRUE) #ordered position of the topics
  topic.top.terms <- lapply(topic.top.topics,function(x) colnames(topic.term.matrix)[x][1:n.terms])
  topic.top.probabilities <- lapply(topic.term.list,sort,decreasing=TRUE)
  topic.top.probabilities <- lapply(topic.top.probabilities,function(x) x[1:n.terms])
  return(list(topic.top.terms=topic.top.terms,topic.top.probabilities=topic.top.probabilities))
}

GetDocumentTopicMatrices <- function(lda.model.list){
  terms.and.topics <- lapply(lda.model.list,posterior)  
  document.topic.matrices <- lapply(terms.and.topics,"[[","topics")
  ordered.document.topic.matrices <- lapply(document.topic.matrices,AuxiliaryOrderDocumentTopicMatrices)
  return(ordered.document.topic.matrices)
}
AuxiliaryOrderDocumentTopicMatrices <- function(document.topic.matrix){
  # This auxiliary function for GetDocumentTopicMatrices turns a DocumentTermMatrix from LDA into a list of ordered numeric vectors and a list of ordered topic names.
  doc.term.list <- apply(document.topic.matrix, 1, as.list)
  doc.term.list <- lapply(doc.term.list,as.numeric) #turn every document of the list into a numeric vector so ordering can be performed
  document.top.topics <- lapply(doc.term.list,order,decreasing=TRUE) #ordered position of the topics
  document.top.probabilities <- lapply(doc.term.list,sort,decreasing=TRUE)
  return(list(document.top.topics=document.top.topics,document.top.probabilities=document.top.probabilities))
}

GetDocumentsAssignedToTopicK <- function(lda.model,k){
  # WARNING: Documents is a distribution over topics. This returns the highest probability for a given topic, but it is possible the 2nd to high topic may have about the same probability!
  all.documents <- topics(lda.model)
  documents.assigned.to.k <- names(all.documents[all.documents == k])
  return(documents.assigned.to.k)
}

############ Parameter Selection Plot Functions #################

PlotLDAModelsPerplexity <- function(lda.model.list){
  # This will calculate the perplexity of the model against itself (TODO: Add a holdout option) for every model in the list, and plot as a line plot. 
  # The perplexity serves to give a single digit value per model (each with a different k, or alpha) representing how well the generative model can generate the documents. Lower value is better.
  # In topicmodels journal, this is used to select the k-value, when it reaches the lowest. 
  # A continuously decreasing curve may suggest the existence of too many topics in the data, perhaps requiring it to be sliced in a smaller subset before creating the LDA model (I guess). 
  perplexities <- sapply(lda.model.list,perplexity)
  plot.table <- data.table(k=1:length(perplexities),perplexity=perplexities)
  p <- ggplot(data=plot.table, aes(x=k, y=perplexity)) + geom_line() + geom_point() + theme_minimal()
  return(p)
}

############# Similarity between Topic Matrices #################
library(lsa)
CalculateHighestTopicCosineSimilarity <- function(ttm1,ttm2){
  # Accepts two topic term matrices generated by different LDA runs. 
  # Topics may have different terms in their respective vocabulary. Non-existent terms will be added with probability 0 to each other.
  ttm1.vocab <- colnames(ttm1)
  ttm2.vocab <- colnames(ttm2)
  ## Which terms of the first vector are NOT in the second vector? Returns the indices. 
  ttm1.vocab.missing.index <- which(!ttm2.vocab %in% ttm1.vocab)
  ttm1.vocab <- c(ttm1.vocab,ttm2.vocab[ttm1.vocab.missing.index])
  # Next we need to add column vectors of probability 0 for every new term on ttm1. We start by creating the matrix.
  ttm1.missing <- matrix(data=0,nrow=nrow(ttm1),ncol=length(ttm1.vocab.missing.index))
  colnames(ttm1.missing) <- ttm2.vocab[ttm1.vocab.missing.index]
  #Then we add the columns to the original matrix. 
  ttm1 <- cbind(ttm1,ttm1.missing) #Notice columns are appended in the end. This results in a unmatching order of columns to ttm2. 
  
  ## Same idea for ttm2
  ttm2.vocab <- colnames(ttm2)
  
  ttm2.vocab.missing.index <- which(!ttm1.vocab %in% ttm2.vocab)
  ttm2.vocab <- c(ttm2.vocab,ttm1.vocab[ttm2.vocab.missing.index])
  
  ttm2.missing <- matrix(data=0,nrow=nrow(ttm2),ncol=length(ttm2.vocab.missing.index))  
  colnames(ttm2.missing) <- ttm1.vocab[ttm2.vocab.missing.index]
  ttm2 <- cbind(ttm2,ttm2.missing)
  
  ## ttm1 columns and ttm2 columns now needs to be ordered so that the vectors for Dkl are consistent
  # Since the vocabularies are now the same, ordering both should result in the same order of words
  ttm1 <- ttm1[,order(ttm1.vocab,decreasing=TRUE)]
  ttm2 <- ttm2[,order(ttm2.vocab,decreasing=TRUE)]
  
  # Next, we must calculate the Cartesian Product of the rows of ttm1 versus the rows of ttm2, i.e. 
  # We compare the similarity of topics of one month versus topics of the other month (but not of the same month, LDAVis package already does that)
  cartesian.ttm1.ttm2.index <- expand.grid(ttm1=1:nrow(ttm1),ttm2=1:nrow(ttm2))
  
  # The number of similarity scores which will be obtained is equal to the number of possible combinations of topic 1 against topic 2.
  similarity <- array(data=NA,dim=nrow(cartesian.ttm1.ttm2.index))
  
  for (i in 1:nrow(cartesian.ttm1.ttm2.index)){
    topic1.index <- cartesian.ttm1.ttm2.index$ttm1[i]
    topic2.index <- cartesian.ttm1.ttm2.index$ttm2[i]
    topic1 <- ttm1[topic1.index,]
    topic2 <- ttm2[topic2.index,]
    similarity[i] <- cosine(topic1,topic2)
  }
  topic.similarity <- as.data.table(cbind(cartesian.ttm1.ttm2.index,similarity))
  
  #Necessary aux function to add ttm2 column for the group by
  aux.highest.similarity <- function(ttm2,similarity){
    index <- which.max(similarity)
    return(list(ttm2=ttm2[index],similarity=similarity[index]))
  }
  highest.topic.similarity <- topic.similarity[,aux.highest.similarity(ttm2,similarity),by=c("ttm1")]
  
  return(highest.topic.similarity)
}


############# LDA Batch #################
# Functions in this block encapsulate functions above to run an entire LDA model from raw data. 


# Used to load the files into memory. Assume the format of the new crawler, where each year of
# mailing list is inside a folder, and months inside sub-folders. 
# See rawToLDA to see it's usage.
loadFiles <- function(raw.corpus.folder.path){
  #Load Required Functions
  
  #Load raw corpus from folder path.
  folder <- readtext(paste0(raw.corpus.folder.path,"/**/*.reply.body.txt"),
                     docvarsfrom = "filepaths"
  )
  # Update file names to remove folder name and extension
  remove_prefix <- sapply(str_split(folder$doc_id,"/"),"[[",2)
  remove_prefix_and_suffix <- sapply(str_split(remove_prefix,"[.]"),"[[",1)
  folder$doc_id <- remove_prefix_and_suffix
  
  return(folder)
}


# Raw to LDA make several assumptions on pre-processing rules. See the lda notebook function for more details.
#
# Arguments
# raw.corpus.folder.path: Path to the folder containing all raw data. 
# k The number of topics k for the model. 
# months A character vector containing the months of interest (currently one uses the first month)
rawToLDA <- function(folder,k,months){
  s <- suppressPackageStartupMessages
  

  
  #Subset in the folder containing all e-mail replies, the months of interest (leverages the fact the Month name is part of the file name)
  month <- months[1]
  is.document.from.month <- grepl(month,folder$doc_id)
  folder.month <- folder[is.document.from.month,]
  
  # Every e-mail reply is a document
  corpus <- corpus(x=folder.month)
  
  #2008_Feb_223.txt 2008_Feb_227.txt 2008_Feb_300.txt 
  #0                0                0 
  
  
  # Tokenize. Several assumptions made here on pre-processing.
  tokens <- tokens(corpus, what = "word", remove_numbers = FALSE, remove_punct = TRUE,
                   remove_symbols = TRUE, remove_separators = TRUE,
                   remove_twitter = FALSE, remove_hyphens = FALSE, remove_url = TRUE)
  tokens <- tokens_tolower(tokens)
  tokens <- removeFeatures(tokens, stopwords("english"))
  
  # Filter Empty Documents
  tokens.length <- sapply(tokens,length)
  tokens <- tokens[!tokens.length == 0]
  
  # DFM
  dfm <- dfm(tokens)
  
  # DFM filter for tokens with nchar > 2 only 
  dfm <-dfm_select(dfm,min_nchar=2,selection="remove")
  
  #LDA
    #TODO: Extend function to select best K based on lowest perplexity. 
    #Ks <- c(10,12) #2:20 # Remember there is no model k=1, always start by 2 or LDA will crash.
    #model.k.for.inspection <- 1 #If the list of models contain only 2 positions, then access it by either 1 or 2. Don't create a Ks <-c(10) and expect to access it at position 10, it will be on position 1! 
  lda.vem <- CalculateLDAModelsInKSet(dfm,k,method="VEM")
  
  model <- list()
  model[["tokens"]] <- tokens
  model[["LDA"]] <- lda.vem[[1]]
  model[["dfm"]] <- dfm #Necessary for LDAVis plot
  
  return(model)
}

##### LDA Vis ######

# Localhost Interactive Topic Visualization
s(require(LDAvis))
plotLDAVis <- function(model,as.gist=FALSE){

  lda.model <- model[["LDA"]]
  lda.model.posterior <- posterior(lda.model)
  
  phi <- lda.model.posterior$terms
  theta <- lda.model.posterior$topics
  
  dfm <- model[["dfm"]]
  doc.length <- as.data.frame(dfm)
  doc.length <- rowSums(doc.length)
  doc.length <- doc.length
  
  vocab <- colnames(phi)
  
  term.frequency <- as.data.frame(dfm)
  term.frequency <- colSums(term.frequency)
  
  json <- createJSON(phi=phi,theta=theta,doc.length=doc.length,vocab=vocab,term.frequency=term.frequency)
  serVis(json=json,open.browser = TRUE,as.gist=as.gist)
}

CalculateTopicFlow <- function(models){
  similarity.list <- list()
  for (i in 2:length(models)){
    #print(i)
    ttm1 <- posterior(models[[i-1]][["LDA"]])$terms
    ttm2 <- posterior(models[[i]][["LDA"]])$terms
    similarity.index <- paste(names(models)[i-1],names(models)[i],sep="_")
    similarity.list[[similarity.index]] <- CalculateHighestTopicCosineSimilarity(ttm1,ttm2)
    colnames(similarity.list[[similarity.index]]) <- c(names(models)[i-1],names(models)[i],paste0(similarity.index,"_similarity"))
    
  }
  
  similarity.df <- similarity.list[[1]]
  for (i in 2:length(similarity.list)){
    #print(i)
    
    # Overlapping column is always second to last on left table
    topic.overlap.x <- colnames(similarity.df)[[ncol(similarity.df)-1]]
    # And first column on right table
    topic.overlap.y <- colnames(similarity.list[[i]])[[1]]
    similarity.df <- merge(similarity.df,similarity.list[[i]],by.x=topic.overlap.x,by.y=topic.overlap.y,all.x=TRUE,all.y=TRUE)
  }
  
  #move Dec column to the left to stay consistent
  dec.index <- ncol(similarity.df)-1
  immediately.before.dec.index <- dec.index-1
  immediately.after.dec.index <- dec.index+1
  similarity.df <- similarity.df[,c(dec.index,1:immediately.before.dec.index,immediately.after.dec.index:ncol(similarity.df)),with=FALSE]
  return(similarity.df)
}

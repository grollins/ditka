library(magrittr)
library(dplyr)
library(tidyr)
library(xlsx)

data <- read.csv("data.csv", stringsAsFactors=FALSE)
QB <- read.delim("2016_rankings/qb.csv", stringsAsFactors=FALSE)
RB <- read.delim("2016_rankings/rb.csv", stringsAsFactors=FALSE)
WR <- read.delim("2016_rankings/wr.csv", stringsAsFactors=FALSE)
TE <- read.delim("2016_rankings/te.csv", stringsAsFactors=FALSE)
K <- read.delim("2016_rankings/k.csv", stringsAsFactors=FALSE)
DEF <- read.delim("2016_rankings/def.csv", stringsAsFactors=FALSE)

data %<>% distinct(full_name)

data %>%
  filter(position == 'QB') %>%
  arrange(desc(points)) %>%
  head(10)

## Get 2015 draft prices

cost_rank <- list()
for (position_str in c('QB', 'RB', 'WR', 'TE', 'K', 'DEF')) {
  print(position_str)
  cost_rank[[position_str]] <- data %>%
    filter(position == position_str) %>%
    arrange(desc(cost)) %>%
    select(cost) %$%
    cost
}

## Apply draft price by position and rank to actual 2015 point rankings

point_rank <- list()
for (position_str in c('QB', 'RB', 'WR', 'TE', 'K', 'DEF')) {
  print(position_str)
  df <- data %>%
    filter(position == position_str) %>%
    arrange(desc(points))
  df$expected_cost <- cost_rank[[position_str]]
  point_rank[[position_str]] <- df
}

point_rank[['QB']]

## save results to excel
wb <- createWorkbook()
cs <- CellStyle(wb) + Font(wb, isBold=TRUE)
for (position_str in c('QB', 'RB', 'WR', 'TE', 'K', 'DEF')) {
  sheet  <- createSheet(wb, sheetName = position_str)
  addDataFrame(point_rank[[position_str]], sheet,
               colnamesStyle = cs, rownamesStyle = cs)
}
saveWorkbook(wb, "counterfactual_2015_draft_prices.xlsx")


## Apply draft price by position and rank to 2016 draft rankings

QB$position <- 'QB'
RB$position <- 'RB'
WR$position <- 'WR'
TE$position <- 'TE'
K$position <- 'K'
DEF$position <- 'DEF'

data2016 <- bind_rows(QB, RB, WR, TE, K, DEF)

data2016 %>% filter(position == 'QB') %>% nrow()
cost_rank[['QB']][1:45]

point_rank <- list()
for (position_str in c('QB', 'RB', 'WR', 'TE', 'K', 'DEF')) {
  print(position_str)
  df <- data2016 %>%
    filter(position == position_str)
  df$expected_cost <- cost_rank[[position_str]][1:nrow(df)]
  point_rank[[position_str]] <- df
}

point_rank[['QB']]

## save results to excel
wb <- createWorkbook()
cs <- CellStyle(wb) + Font(wb, isBold=TRUE)
for (position_str in c('QB', 'RB', 'WR', 'TE', 'K', 'DEF')) {
  sheet  <- createSheet(wb, sheetName = position_str)
  addDataFrame(point_rank[[position_str]], sheet,
               colnamesStyle = cs, rownamesStyle = cs)
}
saveWorkbook(wb, "2016_rankings/draft_prices.xlsx")


library(dplyr)
library(jsonlite)
library(readr)
library(ggplot2)
library(tidyr)
library(testthat)
library(kableExtra)
library(stringr)

# Compute the minimum distance between two elements of a sorted vector in ascending order
min_distance <- function(arr) {
  d <- .Machine$integer.max
  # expect_equal(is.unsorted(arr), FALSE)
  for (i in 1:(length(arr) - 1)) {
    # Compute the distance between consecutive elements
    candidate_d <- abs(arr[i + 1] - arr[i])
    if (candidate_d < d) {
      # we have found a new minimum
      d <- candidate_d
    }
  }
  
  return(d)
}

ny_quick_draw_2013 <- read_csv("../../data/NY_Quick_Draw_2013.csv")

first <- ny_quick_draw_2013[1, ]$`Winning Numbers` %>% str_split(pattern = " ")
length(first[[1]])

quick_draw_number_col_names <- paste("Number", 1:20, sep = "_")

ny_quick_draw_2013_wide <- ny_quick_draw_2013 %>%
  separate(`Winning Numbers`, into = quick_draw_number_col_names,
           sep = " ") 

ny_quick_draw_2013_wide_numeric <- ny_quick_draw_2013_wide %>%
  mutate(across(starts_with("Number_"), as.numeric))

str_for_pasting <- paste("c(", paste(quick_draw_number_col_names, collapse = ", "),
                         ")", sep = "")

ny_quick_draw_2013_with_min_dist <- ny_quick_draw_2013_wide_numeric %>%
  rowwise() %>%
  mutate(min_dist = min_distance(c(Number_1, Number_2, Number_3, Number_4, Number_5, 
                                   Number_6, Number_7, Number_8, Number_9, Number_10, 
                                   Number_11, Number_12, Number_13, Number_14, Number_15, 
                                   Number_16, Number_17, Number_18, Number_19, Number_20)))

ny_quick_draw_2013_observed_counts <- table(ny_quick_draw_2013_with_min_dist$min_dist)

n <- 80
m <- 20

acc <- 0

max_d <- floor((n-1)/(m-1)) - 1
expected_proportions <- vector(mode = "double", length = max_d)

for (i in 1:max_d) {
  prob_less_than_k <- 1 - ( choose(n - i*(m - 1), m) / choose(n, m))
  
  expected_proportions[i] <- prob_less_than_k - acc
  acc <- acc + expected_proportions[i]
}

ny_quick_draw_2013_expected_counts <- expected_proportions * nrow(ny_quick_draw_2013_with_min_dist)
ny_quick_draw_2013_expected_counts_transformed <- c(ny_quick_draw_2013_expected_counts[1], 
ny_quick_draw_2013_expected_counts[2] + ny_quick_draw_2013_expected_counts[3])

ny_quick_draw_2013_test_results <- chisq.test(x = ny_quick_draw_2013_observed_counts, p = ny_quick_draw_2013_expected_counts_transformed,
           rescale.p = TRUE)

ny_quick_draw_2013_test_results$p.value
ny_quick_draw_2013_test_results$parameter

dc_keno_2020 <- read_csv("../../data/DC_Keno_2020.csv")

first_row_dc_2020 <- dc_keno_2020[1, ]$`Winning Numbers` %>% 
  str_split(pattern = " ")
  
dc_keno_number_col_names <- paste("Number", 1:21, sep = "_")

dc_keno_2020_wide <- dc_keno_2020 %>%
  separate(`Winning Numbers`, into = dc_keno_number_col_names,
           sep = " ") %>%
  select(-c("Number_21"))

dc_keno_2020_wide_numeric <- dc_keno_2020_wide %>%
  mutate(across(starts_with("Number_"), as.numeric))

str_for_pasting <- paste("c(", paste(dc_keno_number_col_names, collapse = ", "),
                         ")", sep = "")

# WARNING: DC KENO IS UNSORTED

# dc_keno_2020_with_min_dist <- dc_keno_2020_wide_numeric %>%
#   rowwise() %>%
#   mutate(min_dist = min_distance(c(Number_1, Number_2, Number_3, Number_4, Number_5, 
#                                    Number_6, Number_7, Number_8, Number_9, Number_10, 
#                                    Number_11, Number_12, Number_13, Number_14, Number_15, 
#                                    Number_16, Number_17, Number_18, Number_19, Number_20)))
# 
# dc_keno_2020_with_min_dist_observed_counts <- table(dc_keno_2020_with_min_dist$min_dist)
# 
# n <- 80
# m <- 20
# 
# acc <- 0
# 
# max_d <- floor((n-1)/(m-1)) - 1
# expected_proportions <- vector(mode = "double", length = max_d)
# 
# for (i in 1:max_d) {
#   prob_less_than_k <- 1 - ( choose(n - i*(m - 1), m) / choose(n, m))
#   
#   expected_proportions[i] <- prob_less_than_k - acc
#   acc <- acc + expected_proportions[i]
# }
# 
# ny_quick_draw_2013_expected_counts <- expected_proportions * nrow(ny_quick_draw_2013_with_min_dist)
# ny_quick_draw_2013_expected_counts_transformed <- c(ny_quick_draw_2013_expected_counts[1], 
#                                                     ny_quick_draw_2013_expected_counts[2] + ny_quick_draw_2013_expected_counts[3])
# 
# ny_quick_draw_2013_test_results <- chisq.test(x = ny_quick_draw_2013_observed_counts, p = ny_quick_draw_2013_expected_counts_transformed,
#                                               rescale.p = TRUE)



library(dplyr)
library(jsonlite)
library(readr)
library(testthat)
library(ggplot2)
library(tidyr)

set.seed(1)

german_lotto_numbers_raw <- fromJSON("../../data/LottoNumberArchive/Lottonumbers_tidy_complete.json")

german_lotto_numbers <- german_lotto_numbers_raw %>%
    filter(variable == "Lottozahl")

# sums_for_days <- german_lotto_numbers_raw %>%
#   filter(variable == "Lottozahl") %>%
#   group_by(id) %>%
#   summarise(sum = sum(value))

suffixes <- rep(1:6, times = max(german_lotto_numbers$id))

german_lotto_numbers["rank_of_number"] <- paste(german_lotto_numbers$variable, suffixes, sep="_")

german_lotto_numbers_wide <- german_lotto_numbers %>%
  pivot_wider(id_cols = c(id, date), names_from = rank_of_number, values_from = value)

min_distance <- function(arr) {
  d <- .Machine$integer.max
  for (i in 1:(length(arr) - 1)) {
    candidate_d <- abs(arr[i + 1] - arr[i])
    if (candidate_d < d) {
      d <- candidate_d
    }
  }
  
  return(d)
}

german_lotto_numbers_with_min_dist <- german_lotto_numbers_wide %>%
  rowwise() %>%
  mutate(min_dist = min_distance(c(Lottozahl_1, Lottozahl_2, Lottozahl_3, Lottozahl_4, Lottozahl_5, Lottozahl_6)))

observed_counts <- table(german_lotto_numbers_with_min_dist$min_dist)

expected_proportions <- vector(mode = "double", length = length(observed_counts))

n <- 49
m <- 6

acc <- 0

max_d <- floor((n-1)/(m-1)) - 1
for (i in 1:max_d) {
  prob_less_than_k <- 1 - ( choose(n - i*(m - 1), m) / choose(n, m))
  
  expected_proportions[i] <- prob_less_than_k - acc
  acc <- acc + expected_proportions[i]
}

germany_expected_counts <- expected_proportions * max(german_lotto_numbers_raw$id)
france_expected_counts <- 4858 * expected_proportions
spain_c_expectd_counts <- 6443 * expected_proportions

# transform the data so that d = 7 and d = 8 are grouped together
# so the expected count is greater than 5

germany_expected_counts

germany_expected_counts_transformed <- c(germany_expected_counts[1:6], germany_expected_counts[7] + germany_expected_counts[8])

germany_actual_counts_transformed <- c(observed_counts[1:6], observed_counts[7] + observed_counts[8])

paper_test_results <- chisq.test(germany_actual_counts_transformed, p = germany_expected_counts_transformed, rescale.p = TRUE)

print(paper_test_results$p.value)
print(paper_test_results$parameter)

values_of_d <- c(as.character(1:6), "7 and 8")
expected_counts_for_table <- germany_expected_counts_transformed
actual_counts_for_table <- germany_actual_counts_transformed


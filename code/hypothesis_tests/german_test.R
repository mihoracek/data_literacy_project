library(dplyr)
library(jsonlite)
library(readr)
library(ggplot2)
library(tidyr)
library(testthat)
library(kableExtra)

set.seed(1)

german_lotto_numbers_raw <- fromJSON("../../data/LottoNumberArchive/Lottonumbers_tidy_complete.json")

# We are only interested in the Lottozahl, the 'regular' numbers
german_lotto_numbers <- german_lotto_numbers_raw %>%
    filter(variable == "Lottozahl")

# Verify that the German Lotto dataset is
# sorted in ascending order
are_any_drawings_unsorted <- german_lotto_numbers %>% 
  group_by(id) %>% 
  summarise(unsorted = is.unsorted(value)) %>%
  select(unsorted) %>%
  any()

expect_false(are_any_drawings_unsorted)

# We transform the data so that each row represents one day (i.e. one drawing of 6)
# Each of the 6 numbers will have its own column
suffixes <- rep(1:6, times = max(german_lotto_numbers$id))

# Append indices to produce the column names for the transformed data
german_lotto_numbers["rank_of_number"] <- paste(german_lotto_numbers$variable, suffixes, sep="_")

# Transform the data
german_lotto_numbers_wide <- german_lotto_numbers %>%
  pivot_wider(id_cols = c(id, date), names_from = rank_of_number, values_from = value)

# Compute the minimum distance between two elements of a sorted vector in ascending order
# Because the vector is sorted, we can simply iterate through the vector
# And compare only consecutive elements
min_distance <- function(arr) {
  d <- .Machine$integer.max
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

# Add the minimum distance as a column
german_lotto_numbers_with_min_dist <- german_lotto_numbers_wide %>%
  rowwise() %>%
  mutate(min_dist = min_distance(c(Lottozahl_1, Lottozahl_2, Lottozahl_3, Lottozahl_4, Lottozahl_5, Lottozahl_6)))

# Count the occurrences of the values of d
observed_counts <- table(german_lotto_numbers_with_min_dist$min_dist)

# Compute the expected distribution of d
n <- 49
m <- 6

acc <- 0

max_d <- floor((n-1)/(m-1)) - 1

expected_proportions <- vector(mode = "double", length = max_d)

for (i in 1:max_d) {
  prob_less_than_k <- 1 - ( choose(n - i*(m - 1), m) / choose(n, m))
  
  expected_proportions[i] <- prob_less_than_k - acc
  acc <- acc + expected_proportions[i]
}

germany_expected_counts <- expected_proportions * max(german_lotto_numbers_raw$id)
france_expected_counts <- 4858 * expected_proportions
spain_c_expected_counts <- 6443 * expected_proportions

# transform the data so that d = 7 and d = 8 are grouped together
# so the expected count is greater than 5

germany_expected_counts_transformed <- c(germany_expected_counts[1:6], germany_expected_counts[7] + germany_expected_counts[8])
germany_observed_counts_transformed <- c(observed_counts[1:6], observed_counts[7] + observed_counts[8])

# conduct the test
paper_test_results <- chisq.test(germany_observed_counts_transformed, p = germany_expected_counts_transformed, 
                                 rescale.p = TRUE)

print(paper_test_results$p.value)
print(paper_test_results$statistic)
print(paper_test_results$parameter)

# produce the table for the report
values_of_d <- c(as.character(1:6), "7 and 8")
expected_counts_for_table <- germany_expected_counts_transformed
observed_counts_for_table <- germany_observed_counts_transformed

table_for_report <- data.frame("d" = values_of_d,
           "Expected frequency" = expected_counts_for_table,
           "Actual frequency" = observed_counts_for_table,
           check.names = FALSE) %>%
  t()

# rownames(table_for_report) <- NULL
colnames(table_for_report) <- NULL

kbl_code <- kbl(table_for_report, booktabs = T, format = "latex",
                caption = "Frequencies of $d$ statistic for German Lotto")

print(kbl_code)

library(dplyr)
library(jsonlite)
library(readr)
library(testthat)
library(ggplot2)

set.seed(1)

german_lotto_numbers_raw <- fromJSON("../../data/LottoNumberArchive/Lottonumbers_tidy_complete.json")

n_sims <- 1000000

# sim_of_sums <- replicate(n_sims, sum(sample(1:49, 6, replace=FALSE)))

# bin_cutoffs <- quantile(sim_of_sums, probs = (0:25)/25, na.rm=FALSE)

# bin_cutoffs["0%"] = sum(1:6)
# bin_cutoffs["100%"] = sum(44:49)

# length(unique(bin_cutoffs)) == length(bin_cutoffs)

# length(sim_of_sums[sim_of_sums <= 83]) / n_sims

# I want a data frame where the rows are days, and there is a column variable "sum" with the sum of numbers for that day

sums_for_days <- german_lotto_numbers_raw %>%
  filter(variable == "Lottozahl") %>%
  group_by(id) %>%
  summarise(sum = sum(value))

# sums_for_days %>%
#   summarise()

# cut_ex <- cut(sums_for_days$sum, breaks = bin_cutoffs)
# sum(is.na(cut_ex))

# cut_number(sim_of_sums, n = 10, breaks = bin_cutoffs)

# experimetn
# x <- runif(1000, 0, 10)
# cut_output <- cut(x, breaks = 0:10)
# sum(is.na(cut_output))

# sim_of_sums_for_ef <- replicate(n_sims, sum(sample(1:49, 6, replace=FALSE)))

# sim_cut <- cut(sim_of_sums_for_ef, breaks = bin_cutoffs)

# table(sim_cut)

# Compute the frequencies exactly

# n_rows <- choose(49, 6)
# n_cols <- 6
# lottery_possibilities <- matrix(nrow = n_rows, ncol = n_cols)

possible_lottery_draws <- combn(1:49, 6)

possible_lottery_sums <- colSums(possible_lottery_draws)

counts_of_sums <- table(possible_lottery_sums)

true_bin_cutoffs <- quantile(possible_lottery_sums, probs = (0:25)/25, na.rm=FALSE)

cut_of_all_possibilities <- cut(possible_lottery_sums, breaks = true_bin_cutoffs)
expected_proportions <- table(cut_of_all_possibilities) / length(possible_lottery_sums)
cut_of_german_data <- cut(sums_for_days$sum, breaks = true_bin_cutoffs)
observed_counts <- table(cut_of_german_data)

n_lottery_days <- nrow(sums_for_days)
true_props <- table(cut_of_all_possibilities) / length(possible_lottery_sums)
expected_frequencies <- true_props * n_lottery_days

test_results_with_binning <- chisq.test(x = observed_counts,
                                        correct = FALSE, p = expected_frequencies,
                                        rescale.p = TRUE, simulate.p.value = FALSE)

test_results_with_binning$p.value
test_results_with_binning$parameter

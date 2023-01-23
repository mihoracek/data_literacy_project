library(dplyr)
library(jsonlite)
library(readr)

N_LOTTO_NUMBERS_IN_BOWL <- 49
N_LOTTO_NUMBERS_DRAWN <- 6

german_lotto_numbers <- fromJSON("../../data/LottoNumberArchive/Lottonumbers_tidy_complete.json") %>%
  filter(variable == "Lottozahl") %>% 
  count(value)

# write_csv(german_lotto_numbers, "german_lotto_numbers-from_submodule.csv")

nrow(german_lotto_numbers) == N_LOTTO_NUMBERS_IN_BOWL

german_lotto_number_counts <- german_lotto_numbers$n

expected_proportions <- rep(1/N_LOTTO_NUMBERS_IN_BOWL, times = N_LOTTO_NUMBERS_IN_BOWL)

test_results <- chisq.test(x = german_lotto_number_counts,
                           correct = FALSE, p = expected_proportions,
                           rescale.p = FALSE, simulate.p.value = FALSE)

test_results$p.value
test_results$parameter


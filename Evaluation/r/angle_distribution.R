library(ggplot2)
library(dplyr)
library(tidyr)
library(viridis)
library(ggpubr)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


plot_eer <- function(df, base_name, postfix, title) {
  outfile = paste(base_name, "equal_error_rate", postfix, sep = "_")
  outfile = paste(outfile, ".png", sep = "")
  
  eer_row = head(df %>% mutate(delta = abs(
    false_acceptance_rate - false_rejection_rate
  )) %>% arrange(delta), n = 1)
  eer = (eer_row$false_acceptance_rate + eer_row$false_rejection_rate) / 2
  
  ggplot(df, aes(x = threshold)) +
    geom_point(aes(y = false_acceptance_rate, color = "FAR")) +
    geom_point(aes(y = false_rejection_rate, color = "FRR")) +
    geom_hline(yintercept = eer, linetype = "dashed") +
    annotate(
      "text",
      x = eer_row$threshold - 0.05,
      y = eer + 0.05,
      label = paste("EER = ", round(eer, 3), sep = "")
    ) +
    theme_minimal() +
    theme(legend.title = element_blank()) +
    coord_cartesian(xlim = c(
      max(eer_row$threshold - 0.1, 0),
      min(eer_row$threshold + 0.1, 1)
    )) +
    labs(
      x = "Threshold",
      y = "FAR / FRR",
      title = title,
      subtitle = "Thresholds in [0, 1]"
    ) +
    ggsave(outfile, dpi = "print")
}

calc_eer <- function(df) {
  eer_row = head(df %>% mutate(delta = abs(
    false_acceptance_rate - false_rejection_rate
  )) %>% arrange(delta), n = 1)
  eer = (eer_row$false_acceptance_rate + eer_row$false_rejection_rate) / 2
  
  return(list(eer = eer, threshold = eer_row$threshold))
}

base_name = "../results/plots/"



# Isolated thresholds
threshold_5 = read.csv("../results/5_all.csv", header = FALSE)
threshold_10 = read.csv("../results/10_all.csv", header = FALSE)
threshold_15 = read.csv("../results/15_all.csv", header = FALSE)
threshold_20 = read.csv("../results/20_all.csv", header = FALSE)
threshold_50 = read.csv("../results/50_all.csv", header = FALSE)
threshold_100 = read.csv("../results/100_all.csv", header = FALSE)
threshold_200 = read.csv("../results/200_all.csv", header = FALSE)
precision = c((sapply(threshold_5[5], mean)),
              (sapply(threshold_10[5], mean)),
              (sapply(threshold_15[5], mean)),
              (sapply(threshold_20[5], mean)),
              (sapply(threshold_50[5], mean)),
              (sapply(threshold_100[5], mean)),
              (sapply(threshold_200[5], mean)))

recall = c((sapply(threshold_5[6], mean)),
           (sapply(threshold_10[6], mean)),
           (sapply(threshold_15[6], mean)),
           (sapply(threshold_20[6], mean)),
           (sapply(threshold_50[6], mean)),
           (sapply(threshold_100[6], mean)),
           (sapply(threshold_200[6], mean)))
thresholds = c(5, 10, 15, 20, 50, 100, 200)
df <- data.frame(thresholds, precision, recall)
outfile = "../results/plots/precision_recall.png"

ggplot(df, aes_string(x = "thresholds")) +
  geom_line(aes(y = precision, color = "Precision")) +
  geom_line(aes(y = recall, color = "Recall")) +
  geom_vline(xintercept = 30, linetype="dashed") +
  scale_colour_manual(
    name = "",
    values = c("purple", "red"),
    labels = c(precision, recall)
  ) +
  labs(
    x = "Threshold",
    y = "Prec. / Rec. Score",
    subtitle = "Average of 3 Runs; 100 Random Terms"
  ) + ggsave(outfile, dpi = "print")

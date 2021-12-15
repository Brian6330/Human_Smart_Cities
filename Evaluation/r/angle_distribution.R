library(ggplot2)
library(dplyr)
library(tidyr)
library(viridis)
library(ggpubr)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


aggregate_precision_recall <- function(df_raw) {
  thresholds = unique(df_raw$similarity)
  
  df = data.frame()
  for (t in thresholds) {
    df = rbind(df, evaluate_precision_recall(df_raw, t))
  }
  
  return(df)
}

plot_precision_recall <- function(df, base_name, postfix, title) {
  outfile = paste(base_name, "precision_recall", postfix, sep="_")
  outfile = paste(outfile, ".png", sep="")
  
  max_prec_recall = head(df %>% mutate(delta = abs(precision - recall)) %>% arrange(delta), n=1)
  
  ggplot(df, aes(x = recall, y = precision)) +
    geom_point(size=0.1) +
    geom_vline(xintercept = max_prec_recall$recall, linetype = "dashed") +
    geom_hline(yintercept = max_prec_recall$precision, linetype = "dashed") +
    annotate("text", x = max_prec_recall$recall + 0.04, y = max_prec_recall$precision + 0.02, label = round(max_prec_recall$recall, 3)) +
    theme_minimal() +
    coord_cartesian(xlim = c(0, 1), ylim = c(0, 1)) +
    labs(y = "Precision", x = "Recall", title = title, subtitle = "Thresholds in [0, 1]") +
    ggsave(outfile, dpi = "print")
}

plot_eer <- function(df, base_name, postfix, title) {
  outfile = paste(base_name, "equal_error_rate", postfix, sep="_")
  outfile = paste(outfile, ".png", sep="")
  
  eer_row = head(df %>% mutate(delta = abs(false_acceptance_rate - false_rejection_rate)) %>% arrange(delta), n=1)
  eer = (eer_row$false_acceptance_rate + eer_row$false_rejection_rate) / 2
  
  ggplot(df, aes(x = threshold)) +
    geom_point(aes(y = false_acceptance_rate, color = "FAR")) +
    geom_point(aes(y = false_rejection_rate, color = "FRR")) +
    geom_hline(yintercept = eer, linetype = "dashed") +
    annotate("text", x = eer_row$threshold - 0.05, y = eer + 0.05, label = paste("EER = ", round(eer, 3), sep="")) +
    theme_minimal() +
    theme(legend.title = element_blank()) +
    coord_cartesian(xlim = c(max(eer_row$threshold - 0.1, 0), min(eer_row$threshold + 0.1, 1))) +
    labs(x = "Threshold", y = "FAR / FRR", title = title, subtitle = "Thresholds in [0, 1]") +
    ggsave(outfile, dpi = "print")
}

calc_eer <- function(df) {
  eer_row = head(df %>% mutate(delta = abs(false_acceptance_rate - false_rejection_rate)) %>% arrange(delta), n=1)
  eer = (eer_row$false_acceptance_rate + eer_row$false_rejection_rate) / 2
  
  return(list(eer = eer, threshold = eer_row$threshold))
}

base_name = "../results/plots/"

# max_line_gap= 0
df_0_raw = read.csv("../data/angle_distribution_full.csv")
df_0 = aggregate_precision_recall(df_0_raw)
plot_0 = plot_precision_recall(df_0, base_name, "0", "Angle_Dist(max_line_gap = 0)")
plot_0
plot_0_eer = plot_eer(df_0, base_name, "0_small", "Angle_Dist(max_line_gap = 0)")
plot_0_eer




# Manually defined df containing max line gap / EER from graphs above
df_angle_dist_report = data.frame(
  max_line_gap = c(0, 1, 3, 5, 10),
  eer = c(0.428, 0.523, 0.52, 0.505, 0.478)
)

ggplot(df_angle_dist_report, aes(x = max_line_gap, y = eer)) +
  geom_point(size=3) +
  scale_y_continuous(limits = c(0.35, NA), labels = scales::percent) +
  theme_minimal() +
  labs(y = "EER", x = "Maximum line gap") +
  ggsave("../resources/angle_dist/report_summary.png", dpi = "print")


# Feature in isolation for comparison
threshold_5 = read.csv("../results/5_all.csv", header=FALSE)
threshold_10 = read.csv("../results/10_all.csv", header=FALSE)
threshold_15 = read.csv("../results/15_all.csv", header=FALSE)
threshold_20 = read.csv("../results/20_all.csv", header=FALSE)
threshold_50 = read.csv("../results/50_all.csv", header=FALSE)
threshold_100 = read.csv("../results/100_all.csv", header=FALSE)
threshold_200 = read.csv("../results/200_all.csv", header=FALSE)
precision = c(
  (sapply(threshold_5[5], mean)),
  (sapply(threshold_10[5], mean)),
  (sapply(threshold_15[5], mean)),
  (sapply(threshold_20[5], mean)),
  (sapply(threshold_50[5], mean)),
  (sapply(threshold_100[5], mean)),
  (sapply(threshold_200[5], mean))
)

recall = c(
  (sapply(threshold_5[6], mean)),
  (sapply(threshold_10[6], mean)),
  (sapply(threshold_15[6], mean)),
  (sapply(threshold_20[6], mean)),
  (sapply(threshold_50[6], mean)),
  (sapply(threshold_100[6], mean)),
  (sapply(threshold_200[6], mean))
)
thresholds = c(5,10,15,20,50,100,200)
df <- data.frame(thresholds, precision, recall)
outfile = "../results/plots/precision_recall.png"

ggplot(df, aes_string(x = "thresholds")) + 
  geom_line(aes(y=precision, color = "Precision")) + 
  geom_line(aes(y=recall, color = "Recall")) + 
  
  scale_colour_manual(name = "", values = c("black","red"), labels = c(precision, recall)) +
  labs(
    x = "Threshold",
    y = "Score",
    title = "Precision / Recall vs. Threshold",
    subtitle = "Average of 3 Runs; 100 Random Terms"
  ) + ggsave(outfile, dpi = "print")


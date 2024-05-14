# Load the necessary libraries
library(ergm)
library(base64enc)

# Read the model from the RDS file
results <- readRDS("dump/ergm_results.rds")
model <- results$model

# Read the number of simulations from the text file
num_simulations <- as.integer(readLines("dump/num_simulations.txt"))

# Run the simulations
simulated_networks <- simulate(model, nsim = num_simulations)

# Capture the summary output
summary_output <- capture.output(summary(simulated_networks))

# Calculate the observed and simulated mean statistics
obs_stats <- model$nw.stats
sim_stats <- colMeans(attr(simulated_networks, "stats"))

# Combine the observed and simulated statistics into a data frame
stats_df <- data.frame(
  rbind("obs"= obs_stats, "sim mean"= sim_stats)
)


#-----------------------------------------------------------------------------
# Create a temporary file to store the PNG plot
png_file <- tempfile(fileext = ".png")

# Save the network plot as a PNG file
png(png_file, width = 1200, height = 1200, res = 200)

# Plot the network using the network package
plot(model$network, vertex.cex = 1, vertex.col = "lightblue", edge.col = "gray",
     main = paste("Original Network"))

# Close the PNG device
dev.off()

# Read the PNG file as base64-encoded string
base64_original_plot <- base64enc::dataURI(file = png_file, mime = "image/png")

#-----------------------------------------------------------------------------
# Save the simulated networks, summary output, and statistics in a new RDS file
saveRDS(list(
  simulated_networks = simulated_networks,
  summary_output = summary_output,
  stats_df = stats_df
), file = "dump/simulated_networks.rds")

print("Done!")
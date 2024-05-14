# Load the necessary libraries
library(network)
library(base64enc)

# Read the simulated networks from the RDS file
simulated_networks <- readRDS("dump/simulated_networks.rds")$simulated_networks

# Read the number of chosen network from the text file
selected_network <- as.integer(readLines("dump/selected_network.txt"))

# Get the selected individual simulated network
simulated_network <- simulated_networks[[selected_network]]

# Convert the simulated network to a network object
network_obj <- network(simulated_network)

# Create a temporary file to store the PNG plot
png_file <- tempfile(fileext = ".png")

# Save the network plot as a PNG file
png(png_file, width = 1200, height = 1200, res = 200)

# Plot the network using the network package
plot(network_obj, vertex.cex = 1, vertex.col = "lightblue", edge.col = "gray",
     main = paste("Simulated Network", selected_network))

# Close the PNG device
dev.off()

# Read the PNG file as base64-encoded string
base64_plot <- base64enc::dataURI(file = png_file, mime = "image/png")
print("Done!")
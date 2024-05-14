# Set the default CRAN mirror
options(repos = c(CRAN = "https://cran.r-project.org/"))

library(statnet)
library(network)
library(ergm)
library(networkDynamic)
library(tergm)
library(ergm.count)
library(sna)
library(tsna)
library(Rglpk)

# Read network edge list and attribute data from CSV files
r_edgelist <- read.csv("pages/data/network_edges.csv")
r_attr <- read.csv("pages/data/network_data.csv")

# Create a network object from the edge list
sn_network <- as.network(r_edgelist)

# Set vertex attributes for the network
sn_network <- set.vertex.attribute(sn_network, "vertex.names", r_attr$Name)
sn_network <- set.vertex.attribute(sn_network, "age", r_attr$Age)
sn_network <- set.vertex.attribute(sn_network, "gender", r_attr$Gender)
sn_network <- set.vertex.attribute(sn_network, "education", r_attr$Education)

# Read the formula string from the file
formula_str <- readLines("dump/formula.txt")

# Print the formula string for debugging
print(paste("Formula string from file:", formula_str))

# Construct the formula object using the formula string
formula <- as.formula(paste("sn_network ~", formula_str))

# Print the constructed formula for debugging
print(paste("Constructed formula:", deparse(formula)))


# Fit the ERGM model
model <- ergm(formula)

# Extract summary elements from the model
summary <- summary(model)
coefficients <- coef(summary)
term_names <- rownames(coefficients)

# Perform goodness-of-fit assessment for model2
modelgof <- gof(model)

# Save the results as an RDS file
saveRDS(list(
  model = model,
  model_formula = formula,
  model_coefficients = coefficients,
  term_names = term_names,
  model_gof = modelgof
), file = "dump/ergm_results.rds")

print("ERGM model fitting and evaluation complete.")
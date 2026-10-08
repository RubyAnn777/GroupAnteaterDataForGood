# Gold mining in the Amazon: starter (R version)
# Data for Good, Sessions 3 to 5. Run this once, top to bottom, before you do anything else.
#
# It does four things:
#   1. loads the six shared tables and reproduces the numbers the publishers show
#      (if a check fails, stop and find out why before you go on);
#   2. shows the difference between a LEVEL (hectares classified as mining in a year)
#      and an ADDITION (the change from the year before);
#   3. builds a before/after table with a comparison group;
#   4. draws one figure.
#
# Base R only, no packages. Set the working directory to this file's folder first:
# RStudio menu Session > Set Working Directory > To Source File Location.
# gold_starter.py does the same steps in Python.

data_dir <- if (dir.exists("../data")) "../data" else "data"
read_table <- function(name) read.csv(file.path(data_dir, name), encoding = "UTF-8")

prices_m  <- read_table("prices_monthly.csv")            # world prices, one row per month
prices    <- read_table("prices_annual.csv")             # world prices, one row per year
substance <- read_table("mining_area.csv")               # Brazil: mining by type and substance
br        <- read_table("brazil_municipality_year.csv")  # Brazil: municipality x biome x year
pe        <- read_table("peru_department_year.csv")      # Peru: department x biome x year
zb        <- read_table("peru_bufferzone_year.csv")      # Peru: buffer zone x department x year

cat("Rows:", nrow(prices_m), nrow(prices), nrow(substance), nrow(br), nrow(pe), nrow(zb), "\n")

# ---- 1. Check against the source ------------------------------------------------------
# Each number below can be read off the publisher's own screen (see DOWNLOAD_LOG.csv).
# Your brief reports one such check for every dataset you use, including the ones you add.

check <- function(label, value, expected) {
  ok <- abs(value - expected) < 1
  cat(if (ok) "OK  " else "FAIL", label, ":", format(round(value), big.mark = ","),
      "(publisher:", format(expected, big.mark = ","), ")\n")
  if (!ok) stop("Check failed: ", label)
}

check("Gold price, August 2026, $ per troy ounce",
      prices_m$gold[nrow(prices_m)], 4411)
check("Brazil, mining class, all municipalities, 2024, ha",
      sum(br$mining_ha[br$year == 2024]), 609637)
check("Peru, Madre de Dios, mining class, 2025, ha",
      sum(pe$mining_ha[pe$department == "Madre de Dios" & pe$year == 2025]), 112622)
check("Peru, Tambopata buffer zone, mining class, 2025, ha",
      sum(zb$mining_ha[zb$buffer_zone == "Tambopata" & zb$year == 2025]), 20730)
check("Brazil, artisanal mining (garimpo), 2025, ha",
      sum(substance$mining_artisanal_ha[substance$territory == "Brasil" & substance$year == 2025]), 445987)
check("Brazil, artisanal mining in all indigenous lands, 2025, ha",
      sum(substance$mining_artisanal_ha[substance$territory == "all indigenous lands combined" &
                                          substance$year == 2025]), 39915)

# ---- 2. Levels and additions -------------------------------------------------------------
# The satellite product records the area CURRENTLY classified as mining. That is a stock.
# It almost never falls, so it trends upwards, and so does the gold price. Two series that
# both trend upwards are correlated whatever the truth is. The quantity that answers "how
# much new mining was there this year?" is the ADDITION: this year's level minus last year's.
# A department can appear in several rows per year (one per biome), so add up first.

mdd <- aggregate(mining_ha ~ year, data = pe[pe$department == "Madre de Dios", ], FUN = sum)
mdd <- merge(mdd, prices[, c("year", "gold")], by = "year")   # add the gold price
mdd <- mdd[order(mdd$year), ]
mdd$addition_ha <- c(NA, diff(mdd$mining_ha))                 # level minus last year's level
print(round(mdd[mdd$year >= 2010, ]), row.names = FALSE)

# ---- 3. Before and after, with a comparison group ----------------------------------------
# Operation Mercurio (February 2019) targeted La Pampa, which lies in the buffer zone of the
# Tambopata National Reserve. The Amarakaeri buffer zone, the other large mining front in
# Madre de Dios, was not targeted. Four numbers: the mean annual addition in each zone, in
# the three years before and the three years after. The last line is a difference in
# differences computed by hand. It is a description. See "Why it could mislead" on the
# Question 2 card before you interpret it.

two_zones <- zb[zb$buffer_zone %in% c("Tambopata", "Amarakaeri"), ]
zones <- aggregate(mining_ha ~ buffer_zone + year, data = two_zones, FUN = sum)  # a zone can span two departments
zones <- zones[order(zones$buffer_zone, zones$year), ]
zones$addition_ha <- ave(zones$mining_ha, zones$buffer_zone, FUN = function(x) c(NA, diff(x)))
zones$period <- NA
zones$period[zones$year %in% 2016:2018] <- "2016-18"
zones$period[zones$year %in% 2019:2021] <- "2019-21"

in_window <- zones[!is.na(zones$period), ]
tab <- tapply(in_window$addition_ha, list(in_window$buffer_zone, in_window$period), mean)
change <- tab[, "2019-21"] - tab[, "2016-18"]
print(round(cbind(tab, change)))
cat("Change in Tambopata minus change in Amarakaeri:",
    round(change[["Tambopata"]] - change[["Amarakaeri"]]), "ha per year\n")

# ---- 4. One figure -----------------------------------------------------------------------
# Two panels with a common time axis (not two y-axes in one panel) and a title.
# Your brief has one figure, which should make your main point.

dir.create("output", showWarnings = FALSE)
p <- mdd[mdd$year >= 2001, ]
png("output/starter_figure.png", width = 8, height = 5.5, units = "in", res = 200)
par(mfrow = c(2, 1), mar = c(2.5, 6, 2.5, 1), las = 1, bty = "l")
plot(p$year, p$gold, type = "l", lwd = 2, col = "#234A76", ylim = c(0, max(p$gold)),
     xlab = "", ylab = "")
title("Madre de Dios: the gold price and the new mining area each year", adj = 0, font.main = 1, cex.main = 1)
mtext("Gold price ($ per troy ounce)", side = 2, line = 4.5, las = 0, cex = 0.8)
barplot(p$addition_ha, names.arg = p$year, col = "#F28E2B", border = "#E67E22", ylim = c(0, 20000))
mtext("New mining area in the year (ha)", side = 2, line = 4.5, las = 0, cex = 0.8)
dev.off()
cat("Saved output/starter_figure.png\n")

# ---- What next -----------------------------------------------------------------------------
# - Open your question card. Do the "Describe" step for your own units and years.
# - Download the table your card asks you to add. Add one row for it to DOWNLOAD_LOG.csv and
#   write a check(...) line for it like the ones above.
# - Keep everything in one script that runs from top to bottom. That file, the log and your
#   raw downloads are your replication folder.

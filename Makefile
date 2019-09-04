# download, unpack, dot plot

# https://www2.census.gov/geo/tiger/TIGER2010BLKPOPHU/tabblock2010_01_pophu.zip
data/zip/tabblock2010_%_pophu.zip:
	mkdir -p $(dir $@)
	wget -O $@ https://www2.census.gov/geo/tiger/TIGER2010BLKPOPHU/tabblock2010_%_pophu.zip


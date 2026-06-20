from .IndexTypes import IndexRegistry, IndexEntry, Search
from philh_myftp_biz.terminal import Log
from . import root

# Clear the search registry
Search.save([])

# Iter through all descendants of root
for p in root.descendants:
    
    # If the path is a directory 
    if p.is_dir:

        registry = IndexRegistry(p)

        Log.INFO(f'Building Registry: {registry}')

        # Clear the directory registry
        registry.save([])

        # Iter through all items in the registry
        for child in registry.children:

            entry = IndexEntry(child)
            
            Log.VERB(f'Adding Entry: {entry}')

            # Append the entry to the directory registry
            registry += entry.JSON

            # Append the entry to the search registry
            Search += entry.JSON


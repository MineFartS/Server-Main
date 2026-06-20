from . import IndexRegistry, IndexEntry, Search
from philh_myftp_biz.terminal import Log
from . import root
from re import sub

# ================================================================================================================
# Update index.json files

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

# ================================================================================================================
# Update web.config

# IIS Config File
config = root.child('web.config')

# List of rules
rules: dict[str, str] = {}

# Iter through all descendants of root
for p in root.descendants:

    # If the path is a media file
    if p.type in ['image', 'video', 'audio']:

        # Get the file extension
        ext = p.ext.lower()

        if ext not in rules:

            Log.VERB(f'Appending IIS Rewrite Rule: {ext=}')

            # Add a rule to the list
            rules[ext] = f"""
                        <rule name="Open '{ext}' in Media Viewer" stopProcessing="true">
                            <match url="^(.+)\\.{ext}$" />
                            <action type="Rewrite" url="/_/Media/" appendQueryString="false" />
                            <conditions>
                                <add input="{{QUERY_STRING}}" pattern="raw=true" negate="true" />
                            </conditions>
                        </rule>
            """

Log.INFO('Saving Modified IIS Configuration')

# Update the configuration code
mcode = sub(
    pattern = r'<rules>(.|\n)*<\/rules>', 
    repl    = f'<rules>{''.join(rules.values())}</rules>', 
    string  = config.open().read()
)

# Save the modified configuration
config.open('w').write(mcode)

#====================================================================

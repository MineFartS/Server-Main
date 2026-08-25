from . import IndexRegistry, IndexEntry, root
from philh_myftp_biz.terminal import Log
from re import sub

# ================================================================================================================
# Update index.json files

Search: list[dict] = []

dirs = [root] + [p for p in root.descendants if p.is_dir]

# Iter through all descendants of root
for p in dirs:

    reg = IndexRegistry(path=p)

    Log.INFO(f'Building Registry: {reg.path}')

    # Clear the directory registry
    reg.list.save([])

    # Iter through all items in the registry
    for child in reg.path.children:

        entry = IndexEntry(child)
        
        Log.VERB(f'Adding Entry: {entry}')

        # Append the entry to the directory registry
        reg.list += entry.JSON

        # Append the entry to the search registry
        Search += [entry.JSON]

root.child('/_/Search/search.json').JSON.save(Search)

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

        p.clear_exif()

        if p.ext not in rules:

            Log.VERB(f'Appending IIS Rewrite Rule: {p.ext=}')

            # Add a rule to the list
            rules[p.ext] = f"""
                        <rule name="Open '{p.ext}' in Media Viewer" stopProcessing="true">
                            <match url="^(.+)\\.{p.ext}$" />
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

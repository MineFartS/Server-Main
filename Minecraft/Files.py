from philh_myftp_biz.web.minecraft import ModrinthMod, FabricMC
from philh_myftp_biz.web import URL
from . import version

files: dict[str, URL] = {}

#========================================================================
# Geyser

files['mods/Geyser.jar'] = ModrinthMod('geyser', version).url

#========================================================================
# Fabric Server

files['fabric-server-launch.jar'] = FabricMC(version).server_jar

#========================================================================
# Floodgate

files['mods/Floodgate.jar'] = ModrinthMod('floodgate', version).url

#========================================================================
# Fabric API

files['mods/Fabric API.jar'] = ModrinthMod('fabric-api', version).url

#========================================================================

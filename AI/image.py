from philh_myftp_biz.terminal import set_package
set_package('E:/AI/')

from philh_myftp_biz.num import nearest_multiple
from diffusers import StableDiffusionPipeline
from philh_myftp_biz.file import temp
from philh_myftp_biz.pc import Path
from . import args, messages
from psutil import Process
from torch import float16

# ====================================================
# PARSE INPUT

args.Arg(
    name = 'model',
    default = 'runwayml/stable-diffusion-v1-5'
)

args.Arg(
    name = 'path',
    default = temp('gen_image', 'png'),
    desc = 'Path to save image',
    handler = Path
)

args.Arg(
    name = 'width',
    default = 512,
    handler = lambda x: nearest_multiple(int(x), 8)
)

args.Arg(
    name = 'height',
    default = 512,    
    handler = lambda x: nearest_multiple(int(x), 8)
)

# ====================================================
# PIPELINE

# Restrict to 2 cores
Process().cpu_affinity([0, 1])

pipeline = StableDiffusionPipeline.from_pretrained(
    pretrained_model_name_or_path = args['model'],
    torch_dtype = float16,
    cache_dir = 'E:/AI/__pycache__/',
    safety_checker = None,
    low_cpu_mem_usage = True
)

pipeline.vae.enable_slicing()

pipeline.to("cuda")

# ====================================================
# GENERATE IMAGE

# Path for output image
imgfile: Path = args['path']

# Prompt the pipeline
prompt = pipeline(
    prompt = messages.prompt(),
    height = args['height'],
    width = args['width']
)

# Save the generated image
prompt.images[0].save(str(imgfile))

# Upload the image to the messages object
messages.add_file(
    role = 'assistant', 
    path = imgfile
)

# ====================================================

messages.output()
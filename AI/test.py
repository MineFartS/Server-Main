import diffusers, torch, psutil

p = psutil.Process()
p.cpu_affinity([0, 1])

# Load the pipeline
pipeline = diffusers.StableDiffusionPipeline.from_pretrained(
    pretrained_model_name_or_path = 'runwayml/stable-diffusion-v1-5',
    torch_dtype = torch.float16,
    cache_dir = 'E:/__temp__/',
    safety_checker = None,
    low_cpu_mem_usage = True
)

pipeline.vae.enable_slicing()

# Move the pipeline to the GPU
pipeline.to("cuda")

# Prompt the pipeline
prompt = pipeline('tree')

# Save the generated image
prompt.images[0].save('E:/AI/test.png')

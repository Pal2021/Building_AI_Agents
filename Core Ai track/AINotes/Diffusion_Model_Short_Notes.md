# Diffusion Model – Short Notes

### What is a Diffusion Model?
- A type of AI model mainly used for **generating high-quality images** (also used for video & audio).
- Works by learning to reverse a process of adding noise to images.

### How it Works

1. **Forward Process** (during training)
   - Takes a real image
   - Gradually adds random noise step-by-step
   - Until the image becomes pure noise

2. **Reverse Process** (during generation)
   - Starts from pure random noise
   - Gradually removes noise step-by-step
   - Finally creates a clean image

### Generation Process
- User gives a text prompt (e.g. “a cat in space”)
- Model starts with random noise
- Removes noise over multiple steps (usually 20–50)
- Outputs a final clear image matching the prompt

### Popular Diffusion Models

| Model              | Type             | Speciality                      |
|--------------------|------------------|---------------------------------|
| Stable Diffusion   | Text-to-Image   | Most popular open-source model |
| FLUX               | Text-to-Image   | Very high image quality        |
| DALL·E             | Text-to-Image   | OpenAI’s closed model          |
| Midjourney         | Text-to-Image   | Artistic high-quality images   |

### Key Advantages
- Excellent image quality
- Strong understanding of text prompts
- Can generate in many styles (realistic, anime, artistic, etc.)
- Open-source versions can run on Google Colab

### Common Use Cases
- Text-to-Image generation
- Image editing & inpainting
- Style transfer
- Video generation (newer models)

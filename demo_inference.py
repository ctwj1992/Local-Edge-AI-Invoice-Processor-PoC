import os
from PIL import Image
from optimum.intel import OVModelForVisualCausalLM
from transformers import AutoProcessor

# --- CONFIGURATION ---
# We use the OpenVINO optimized model path
MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"

def run_demo(image_path):
    print(f"🚀 Loading Edge AI Model: {MODEL_ID}...")
    
    # Load model on local hardware (GPU/NPU)
    model = OVModelForVisualCausalLM.from_pretrained(
        MODEL_ID, 
        device="GPU", 
        trust_remote_code=True
    )
    processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
    
    # Prepare Input
    image = Image.open(image_path)
    
    # Generic Prompt (Hides your specific engineering)
    prompt = "Extract the key data from this document into JSON format."
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt},
            ],
        }
    ]

    # Inference
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], images=[image], padding=True, return_tensors="pt")
    
    print("✨ Analyzing...")
    generated_ids = model.generate(**inputs, max_new_tokens=512)
    output_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    print("\n--- RAW OUTPUT ---")
    print(output_text)

if __name__ == "__main__":
    # Simple check to show it runs
    if os.path.exists("sample_invoice.png"):
        run_demo("sample_invoice.png")
    else:
        print("Please place a 'sample_invoice.png' in this folder to test.")

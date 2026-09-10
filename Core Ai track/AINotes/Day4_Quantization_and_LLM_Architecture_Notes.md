# Day 4 Notes: Quantization + Inside the Brain of LLMs

---

## 1. Quantization

### What is Quantization?
Quantization means reducing the precision of the numbers (weights) used in a model to make it smaller and faster.

### Why do we need it?
- Full precision models are very large.
- Colab free GPU (Tesla T4) has only **15 GB** GPU memory.
- Without quantization, even 7B models struggle to fit.

### Common Precision Types

| Precision     | Bytes per Parameter | Memory Usage | Quality          | Use Case                  |
|---------------|---------------------|--------------|------------------|---------------------------|
| FP32          | 4 bytes             | Very High    | Best             | Rarely used now           |
| FP16 / BF16   | 2 bytes             | High         | Excellent        | High-quality inference    |
| 8-bit         | 1 byte              | Medium       | Very Good        | Good balance              |
| **4-bit**     | 0.5 byte            | Low          | Good             | Best for Colab (Recommended) |

### Popular 4-bit Methods
- **bitsandbytes** (most common with Hugging Face)
- **AWQ**
- **GPTQ**

### Benefits of Quantization
- Less GPU memory usage
- Faster inference
- Ability to run larger models on smaller GPUs
- Makes 7B–14B models run smoothly on Colab T4

---

## 2. Going Inside the Brain of LLMs (LLaMA Architecture)

Modern LLMs (Llama, Phi, Gemma, Qwen, DeepSeek, etc.) are **Decoder-only Transformers**.

### High-Level Structure of LLaMA

1. **Token Embedding Layer**
   - Converts token IDs (numbers) into dense vectors (embeddings)
   - These vectors carry meaning

2. **Stack of Decoder Layers** (Many layers)
   Each Decoder Layer contains:
   
   - **Self-Attention**
     - Allows the model to look at all previous tokens
     - Decides which tokens are important for predicting the next token
     - Uses Query (Q), Key (K), Value (V)

   - **Feed-Forward Network (FFN)**
     - Thinks deeper on the information coming from attention
     - Usually uses SwiGLU activation (in LLaMA)

   - **RMSNorm** (Normalization)
   - **Residual Connections** (Add & Norm)

3. **Final Language Model Head (LM Head)**
   - Converts the final vector into probabilities for the next token

---

### Important Internal Concepts

| Concept              | Simple Meaning                                      |
|----------------------|-----------------------------------------------------|
| Self-Attention       | Model decides what to focus on                      |
| Multi-Head Attention | Looks at information from many different views      |
| Residual Connection  | Helps information flow easily through deep layers   |
| RMSNorm              | Stabilizes training and inference                   |
| Non-Linearity (SwiGLU) | Gives model power to learn complex patterns       |
| RoPE                 | Rotary Positional Embedding (used in LLaMA)         |

---

### Flow of Information (Simple)

```
Input Text
   ↓
Tokenizer → Token IDs
   ↓
Token Embedding
   ↓
Decoder Layer 1 (Attention + FFN)
   ↓
Decoder Layer 2
   ↓
...
   ↓
Decoder Layer N
   ↓
LM Head → Probabilities of next token
   ↓
Select next token → Repeat
```

---

### Key Takeaways

- Quantization (especially 4-bit) is **mandatory** for running good models on Colab.
- LLMs understand text only through embeddings + attention.
- Self-Attention is the heart of the Transformer.
- Residual connections + Normalization make deep models possible.
- Everything finally becomes a prediction of the **next token**.

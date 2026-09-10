# What is Inference Time?

**Inference time** refers to the stage when a model has already been trained and is now being used to **generate answers** or make predictions.

### Simple Comparison

| Stage         | What happens                      | What happens to Parameters                   |
| ------------- | --------------------------------- | -------------------------------------------- |
| **Training**  | The model learns from data        | Parameters keep getting updated              |
| **Inference** | The model is used to give answers | Parameters remain **frozen** (do not change) |

---

### Example

When you chat with ChatGPT, Grok, Claude, or any other AI assistant, the process happening behind the scenes is called **Inference**.

The model takes your question → converts it into tokens → creates embeddings → processes them through the layers → and generates a response.

This entire process is known as **Inference**.

---

### What Happens During Inference?

1. Input text is converted into tokens
2. Tokens are converted into embeddings
3. Embeddings pass through Transformer layers (Attention + Feed Forward Network)
4. The model predicts the next token
5. This process repeats until the full response is generated (auto-regressive generation)

---

### Related Terms You Often Hear

- **Inference Speed**: How fast the model generates tokens (measured in tokens per second)
- **Inference Cost**: How much compute/money it costs to generate one response
- **Inference Optimization**: Techniques like Quantization, KV Cache, Speculative Decoding, etc., that make inference faster and cheaper

---

### Short Summary

- **Training** = Teaching the model
- **Inference** = Using the model (actual real-world usage)

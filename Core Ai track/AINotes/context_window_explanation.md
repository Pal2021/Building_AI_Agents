# What is Context Window?

**Context Window** (also called Context Length) is the maximum amount of text (measured in tokens) that a language model can consider at one time while generating a response.

It acts like the model’s short-term memory.

### Simple Explanation

Just like humans have limited short-term memory, an LLM can only “remember” a limited number of tokens in a single conversation or document.

Anything beyond this limit is either ignored or truncated.

### Technical Explanation

- The Context Window is the maximum number of tokens the model can process in one forward pass (input + generated output combined).
- When the total tokens exceed this limit, older tokens are usually dropped (unless advanced techniques like sliding window attention or memory mechanisms are used).
- Both the user’s input and the model’s previous responses count toward the context window.

### Real-World Examples

| Model             | Context Window    |
| ----------------- | ----------------- |
| GPT-3.5           | 4K tokens         |
| GPT-4 Turbo       | 128K tokens       |
| Claude 3.5 Sonnet | 200K tokens       |
| Gemini 1.5 Pro    | 1 Million+ tokens |
| Llama 3.1 405B    | 128K tokens       |

**Note**: 1 token is roughly equal to 0.75 words in English.  
So a 128K context window can handle approximately 90,000–100,000 words.

### Why Context Window Matters

- Larger context window → Model can handle longer documents, books, codebases, or long conversations.
- Smaller context window → Model forgets earlier parts of the conversation or document.

### Summary

- **Context Window** = How much text the model can “see” and remember at once.
- It is measured in **tokens**, not words or characters.

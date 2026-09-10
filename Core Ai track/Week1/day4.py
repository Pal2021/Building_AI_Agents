import tiktoken

encoding = tiktoken.encoding_for_model("gpt-5.6-sol")

tokens = encoding.encode("Hi my name is Ed and I like banoffee pie")

print(tokens)
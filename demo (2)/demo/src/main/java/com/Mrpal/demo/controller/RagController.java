package com.Mrpal.demo.controller;


import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/rag")
public class RagController {

    private final ChatClient chatClient;
    private final VectorStore vectorStore;

    public RagController(@Qualifier("ragChatClient") ChatClient chatClient,
                         VectorStore vectorStore) {
        this.chatClient = chatClient;
        this.vectorStore = vectorStore;
    }

    @GetMapping
    public String ragChat(@RequestParam String message) {
        // 1. Manually check what the vector store finds
        List<Document> docs = vectorStore.similaritySearch(
                SearchRequest.builder()
                        .query(message)
                        .topK(5)
                        .build());

        System.out.println("DEBUG: Found " + docs.size() + " documents for query: " + message);
        docs.forEach(d -> System.out.println(" - " + d.getText()));

        // 2. Proceed with the call
        return chatClient.prompt()
                .user(message)
                .advisors(QuestionAnswerAdvisor.builder(vectorStore)
                        .searchRequest(SearchRequest.builder()
                                .query(message)
                                .topK(5)
                                .build())
                        .build())
                .call()
                .content();
    }
}
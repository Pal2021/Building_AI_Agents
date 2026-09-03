package com.Mrpal.demo.config;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.google.genai.GoogleGenAiChatOptions;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ChatClientConfig {

    @Bean
    public ChatClient chatClient(@Qualifier("googleGenAiChatModel") ChatModel chatModel) {
        return ChatClient.builder(chatModel)
                .defaultOptions(GoogleGenAiChatOptions.builder()
                        .temperature(0.1)
                        .build())
                .defaultSystem("""
                        You are an internal HR assistant. Your role is to help 
                        employees with questions related to HR policies, such as 
                        leave policies, working hours, benefits, and code of conduct.
                        If a user asks for help with anything outside of these topics, 
                        kindly inform them that you can only assist with queries related to 
                        HR policies.
                        """)
                .build();
    }

    @Bean
    public ChatClient ragChatClient(@Qualifier("googleGenAiChatModel") ChatModel chatModel) {
        return ChatClient.builder(chatModel)
                .defaultOptions(GoogleGenAiChatOptions.builder()
                        .temperature(0.1)
                        .build())
                .defaultSystem("""
                        You are a helpful assistant.
                        Answer the user's question directly using your knowledge.
                        Use any provided context as additional supporting information.
                        Always give a complete and helpful answer.
                        """)
                .build();
    }
}
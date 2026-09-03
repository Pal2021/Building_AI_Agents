package com.spring_ai_tools.spring_ai_tools_calling.controller;

import com.spring_ai_tools.spring_ai_tools_calling.service.ChatService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private final ChatService chatService;

    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    @GetMapping
    public String chat(@RequestParam String message) {
        return chatService.chat(message);
    }
}

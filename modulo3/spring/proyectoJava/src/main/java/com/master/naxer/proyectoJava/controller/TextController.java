package com.master.naxer.proyectoJava.controller;

import com.master.naxer.proyectoJava.service.TextService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TextController {
    @Autowired
    public TextService svc;

    @GetMapping(value = "/printString")
    public String printText() {
        return this.svc.getText();
    }

}

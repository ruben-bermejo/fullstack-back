package com.master.naxer.proyectoJava.controller;

import com.master.naxer.proyectoJava.service.TextService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;

@Controller
public class TextController {
    @Autowired
    private TextService svc;
    public void printText() {
        System.out.println(this.svc.getText());
    }
}

package com.master.naxer.proyectoJava.controller;

import com.master.naxer.proyectoJava.service.TextService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;

@Controller
public class TextController {
    @Autowired
    public TextService svc;
    public void printText() {
        String texto = this.svc.getText();
        System.out.println(texto);
        try {
            svc.getException();
        } catch (Exception e) {
            //do nothing
        }
    }

}

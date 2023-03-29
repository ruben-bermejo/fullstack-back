package com.master.naxer.proyectoJava.service;

import org.springframework.stereotype.Service;

@Service
public class TextService {
    public String getText(){
        return "Hello, world";
    }

    public void getException() throws Exception {
        throw new Exception("Se produjo una excepción");
    }

}

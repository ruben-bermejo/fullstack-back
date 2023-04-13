package com.master.naxer.proyectoJava.service;

import com.master.naxer.proyectoJava.repository.TextRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TextService {

    @Autowired
    TextRepository repository;

    public String getText(){
        return this.repository.getText();
    }

    public void getException() throws Exception {
        throw new Exception("Se produjo una excepción");
    }

}

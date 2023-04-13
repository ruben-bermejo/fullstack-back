package com.master.naxer.proyectoJava.repository;

import org.springframework.stereotype.Repository;

@Repository
public class TextRepository {

    public String getText(){
        return "Hello, World!";
    }

}

package com.master.naxer.service;

import javax.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class HelloWorldService {

    public String getHelloString(){
        return "Hello, World";
    }

}

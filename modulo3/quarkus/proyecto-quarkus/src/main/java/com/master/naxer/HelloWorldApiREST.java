package com.master.naxer;

import com.master.naxer.service.HelloWorldService;

import javax.inject.Inject;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

@Path("/printString")
public class HelloWorldApiREST {

    @Inject
    HelloWorldService service;

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public HelloWorld printString() {
        return new HelloWorld(service.getHelloString());
    }

}

package com.master.naxer.proyectoJava;

import com.master.naxer.proyectoJava.controller.TextController;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class ProyectoJavaApplication {
	public static void main(String[] args) {
		ApplicationContext c = SpringApplication.run(ProyectoJavaApplication.class, args);
		c.getBean(TextController.class).printText();
	}

}

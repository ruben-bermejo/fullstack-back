package com.master.naxer.proyectoJava.aspect;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;
@Aspect
@Component
public class ProyectoJavaAspect {
    @Pointcut("execution(* com.master.naxer.proyectoJava.controller.TextController.printText())")
    public void capturarMetodo() throws Throwable {}

    @Before("capturarMetodo()")
    public void logBeforeGetText(JoinPoint jp){
        System.out.println("AOP: ¡Antes de ejecutar TextController.printText()!");
    }

    @After("capturarMetodo()")
    public void logAfterGetText(JoinPoint jp){
        System.out.println("AOP: ¡Después de ejecutar TextController.printText()!");
    }

    @AfterThrowing(value = "execution(* com.master.naxer.proyectoJava.service.TextService.getException())",
            throwing = "e")
    public void logException(JoinPoint thisJoinPoint, Throwable e) {
        System.out.println("AOP: ¡Excepción en TextService capturada! -> " + e.getMessage());
    }

}

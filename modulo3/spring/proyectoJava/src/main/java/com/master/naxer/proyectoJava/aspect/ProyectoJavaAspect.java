package com.master.naxer.proyectoJava.aspect;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;
@Aspect
@Component
public class ProyectoJavaAspect {
    @Around("execution(public String com.master.naxer.proyectoJava.service.*.*())")
    public Object imprimirMensaje(ProceedingJoinPoint point) throws Throwable {
        System.out.println("Ejecutado el método de TextService!!");
        return point.proceed();
    }

}
